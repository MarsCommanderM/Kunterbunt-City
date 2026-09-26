shader_type canvas_item;
render_mode unshaded, blend_mix;

/* P04-T04: Umfärben pro Teil mit bis zu 3 Farbzonen.
   Die Teil-Textur speichert die ZONEN-GEWICHTE (mit eingebackenem Hell-Dunkel-Verlauf) in R/G/B
   und die Deckung in A. Farbe = R·zone1 + G·zone2 + B·zone3  → Konturen bleiben farbig (Stil C),
   kein Schwarz, keine zweite Textur nötig. */

uniform vec3 zone1 : source_color = vec3(1.0);
uniform vec3 zone2 : source_color = vec3(1.0);
uniform vec3 zone3 : source_color = vec3(1.0);

void fragment() {
	vec4 t = texture(TEXTURE, UV);
	vec3 col = t.r * zone1 + t.g * zone2 + t.b * zone3;
	COLOR = vec4(col, t.a * COLOR.a);
}
