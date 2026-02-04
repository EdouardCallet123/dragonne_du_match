import { Redis } from '@upstash/redis';

// Cette fonction gère les requêtes POST sur /api/vote
export async function onRequestPost(context) {
  try {
    // 1. Récupérer les données envoyées
    const { request, env } = context;
    const body = await request.json();
    const playerId = body.playerId;

    if (!playerId) {
      return new Response("ID manquant", { status: 400 });
    }

    // 2. Connexion à Redis via les variables d'environnement Cloudflare
    const redis = new Redis({
      url: env.UPSTASH_REDIS_REST_URL,
      token: env.UPSTASH_REDIS_REST_TOKEN,
    });

    // 3. Incrémenter le compteur (Vote)
    // On ajoute une date pour pouvoir trier par match si besoin plus tard
    // ex: match_2023-10-24_player_10
    const today = new Date().toISOString().split('T')[0];
    await redis.incr(`match_${today}_player_${playerId}`);

    return new Response(JSON.stringify({ status: "ok" }), {
      headers: { "Content-Type": "application/json" },
    });

  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), { status: 500 });
  }
}