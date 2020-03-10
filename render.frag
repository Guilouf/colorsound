#version 330 core
uniform vec2  iResolution;
uniform sampler2D iChannel0;
out vec4 fragColor;

// Just transmit the image, and add contrast
void main()
{  
	vec2 uv = gl_FragCoord.xy / iResolution.xy;

    fragColor = texture(iChannel0, uv) * vec4(15,15,15,15);
}