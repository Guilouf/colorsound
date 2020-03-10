#version 330 core
/*
Kernel, return rgba as left,right,up,down
Takes a kernel and the current image pixel as input,
returns a kernel
*/
uniform vec2  iResolution;
uniform sampler2D iChannel0;
uniform sampler2D iChannel1;
out vec4 fragColor;

vec2 move(vec2 uv, vec2 xy) {
	return uv + xy / iResolution.xy;
}

void main()
{

    vec2 uv = gl_FragCoord.xy / iResolution.xy;
    vec4 prevK = texture(iChannel0, uv); //previous kernel
    fragColor = prevK;

    //previous pixels
    vec4 center = texture(iChannel1, uv);
    vec4 left = texture(iChannel1, move(uv, vec2(1,0)));
	vec4 right = texture(iChannel1, move(uv, vec2(-1,0)));
    vec4 down = texture(iChannel1, move(uv, vec2(0,1)));
    vec4 up = texture(iChannel1, move(uv, vec2(0,-1)));

    fragColor.a += (center.r - left.r);
    fragColor.r += (center.r - right.r);
    fragColor.g += (center.r - up.r);
    fragColor.b += (center.r - down.r);

}
