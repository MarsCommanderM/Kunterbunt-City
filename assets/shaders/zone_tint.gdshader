shader_type canvas_item;
render_mode unshaded, blend_mix;

/* P04-T04 / P04b: Umfärben pro Teil mit bis zu 3 Farbzonen + Tinte.
   Die Teil-Textur speichert die ZONEN-GEWICHTE (mit eingebackenem Hell-Dunkel) in R/G/B und die Deckung in A.
   Farbe = R·zone1 + G·zone2 + B·zone3 + (1 − R − G − B)·ink
   → Kontur und Schatten laufen in die Tinte (dunkles Braun statt Schwarz). ink = Schwarz ergibt exakt die
   alte Formel (Phase 04), alte Teile bleiben also unverändert.
   Muster (optional): Zone 1 wird innerhalb der Fläche mit pattern_col gemischt (Streifen, Punkte …);
   pattern_scale = Wiederholungen über die Textur (so bleibt das Muster in cm gleich groß). */

uniform vec3 zone1 : source_color = vec3(1.0);
uniform vec3 zone2 : source_color = vec3(1.0);
uniform vec3 zone3 : source_color = vec3(1.0);
uniform vec3 ink : source_color = vec3(0.0);
uniform sampler2D pattern_tex : repeat_enable, filter_linear;
uniform bool has_pattern = false;
uniform vec3 pattern_col : source_color = vec3(1.0);
uniform vec2 pattern_scale = vec2(1.0);

void fragment() {
	vec4 t = texture(TEXTURE, UV);
	vec3 z1 = zone1;
	if (has_pattern) {
		float p = texture(pattern_tex, UV * pattern_scale).a;
		z1 = mix(zone1, pattern_col, p);
	}
	float rest = clamp(1.0 - t.r - t.g - t.b, 0.0, 1.0);
	vec3 col = t.r * z1 + t.g * zone2 + t.b * zone3 + rest * ink;
	COLOR = vec4(col, t.a * COLOR.a);
}
