import { Redis } from '@upstash/redis';

export async function onRequestPost(context) {
  try {
    const { request, env } = context;
    const body = await request.json();
    const playerId = body.playerId;

    if (!playerId) {
      return new Response("ID manquant", { status: 400 });
    }

    // Connexion sécurisée
    const redis = new Redis({
      url: env.UPSTASH_REDIS_REST_URL,
      token: env.UPSTASH_REDIS_REST_TOKEN,
    });

    // Format de la clé : dragonne_match_YYYY-MM-DD_player_ID
    const today = new Date().toISOString().split('T')[0];
    
    // On incrémente le compteur de la joueuse
    await redis.incr(`dragonne_match_${today}_player_${playerId}`);

    return new Response(JSON.stringify({ status: "ok" }), {
      headers: { "Content-Type": "application/json" },
    });

  } catch (err) {
    // En cas d'erreur (rare), on renvoie 500 mais l'utilisateur ne le verra pas
    return new Response(JSON.stringify({ error: err.message }), { status: 500 });
  }
}