#version 330 core
uniform vec2  iResolution;
uniform sampler2D iChannel0;

// Just transmit the image, and add contrast
void mainImage( out vec4 fragColor, in vec2 fragCoord )
{  
	vec2 uv = fragCoord.xy / iResolution.xy;

    fragColor = texture(iChannel0, uv) * vec4(15,15,15,15);
}