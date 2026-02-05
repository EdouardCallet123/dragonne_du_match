import { Redis } from '@upstash/redis';

export async function onRequestPost(context) {
  try {
    const { request, env } = context;
    const { playerId, deviceId } = await request.json(); // On récupère aussi un ID de l'appareil

    if (!playerId || !deviceId) {
      return new Response("Données manquantes", { status: 400 });
    }

    const redis = new Redis({
      url: env.UPSTASH_REDIS_REST_URL,
      token: env.UPSTASH_REDIS_REST_TOKEN,
    });

    // 1. VERIFICATION DU VERROU (Anti-spam 1h)
    const lockKey = `lock_vote_${deviceId}`;
    const hasVotedRecently = await redis.get(lockKey);

    if (hasVotedRecently) {
      return new Response(JSON.stringify({ error: "Vous devez attendre 1h" }), { status: 429 });
    }

    // 2. ENREGISTREMENT DU VOTE
    const today = new Date().toISOString().split('T')[0];
    const voteKey = `results_${today}`;
    
    // On utilise un HINCRBY pour stocker tous les joueurs dans la même table du jour
    // C'est BEAUCOUP plus facile à analyser ensuite
    await redis.hincrby(voteKey, playerId, 1);

    // 3. MISE EN PLACE DU CACHE DE 1H
    // On crée une clé vide qui expire dans 3600s
    await redis.set(lockKey, "true", { ex: 3600 });

    return new Response(JSON.stringify({ status: "ok" }), {
      headers: { "Content-Type": "application/json" },
    });

  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), { status: 500 });
  }
}