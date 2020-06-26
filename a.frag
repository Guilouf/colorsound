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

    left.r = floatEq(left.g, 0.) ? left.r : center.r;
    right.r = floatEq(right.g, 0.) ? right.r : center.r;
    down.r = floatEq(down.g, 0.) ? down.r : center.r;
    up.r = floatEq(up.g, 0.) ? up.r : center.r;

    fragColor.a += (center.r - left.r);
    fragColor.r += (center.r - right.r);
    fragColor.g += (center.r - up.r);
    fragColor.b += (center.r - down.r);

}
