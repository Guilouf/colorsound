#version 330 core
/*
Kernel, return rgba as left,right,up,down
Takes a kernel and the current image pixel as input,
returns a kernel
*/
uniform vec2  iResolution;
uniform sampler2D kernelTexture;
uniform sampler2D iChannel1;
out vec4 fragColor;

vec2 move(vec2 uv, vec2 xy) {
	return uv + xy / iResolution.xy;
}

bool floatEq(float value, float to_compare) {
    return abs(value - to_compare) < 0.00000000001;
}

void main()
{

    vec2 uv = gl_FragCoord.xy / iResolution.xy;
    vec4 prevK = texture(kernelTexture, uv); //previous kernel
    fragColor = prevK;

    //previous pixels, we could use only vec2
    vec4 center = texture(iChannel1, uv);
    vec4 left = texture(iChannel1, move(uv, vec2(1,0)));
	vec4 right = texture(iChannel1, move(uv, vec2(-1,0)));
    vec4 down = texture(iChannel1, move(uv, vec2(0,1)));
    vec4 up = texture(iChannel1, move(uv, vec2(0,-1)));

    // nearby walls to 0
    fragColor.a += floatEq(left.g, 0.) ? (center.r - left.r) : 0;
    fragColor.r += floatEq(right.g, 0.) ? (center.r - right.r) : 0;
    fragColor.g += floatEq(up.g, 0.) ? (center.r - up.r) : 0;
    fragColor.b += floatEq(down.g, 0.) ? (center.r - down.r) : 0;

    // if it's a wall, do nothing
    fragColor = floatEq(center.g, 0.) ? fragColor : prevK;

}
