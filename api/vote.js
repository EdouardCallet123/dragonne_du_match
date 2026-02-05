import { Redis } from '@upstash/redis';

export async function onRequestPost(context) {
  const { env } = context;
  
  const redis = new Redis({
    url: env.UPSTASH_REDIS_REST_URL,
    token: env.UPSTASH_REDIS_REST_TOKEN,
  });

  try {
    // TEST DE CONNEXION : On écrit une clé fixe
    await redis.set("test_connexion", "ca_marche_" + new Date().getTime());
    
    // Ton code de vote
    const body = await request.json();
    const playerId = body.playerId;
    const today = new Date().toISOString().split('T')[0];
    const key = `dragonne_match_${today}_player_${playerId}`;
    
    await redis.incr(key);

    return new Response(JSON.stringify({ status: "Vote enregistré !" }), { status: 200 });
  } catch (err) {
    return new Response(JSON.stringify({ error: "Erreur Redis: " + err.message }), { status: 500 });
  }
}