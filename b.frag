#version 330 core
/*
Image buffer
Takes previous image and kernel as input,
returns a new image
*/
uniform vec2  iMouse;
uniform vec2  iResolution;
uniform sampler2D iChannel0;
uniform sampler2D iChannel1;
out vec4 fragColor;

void main()
{  
	vec2 uv = gl_FragCoord.xy / iResolution.xy;
    ivec2 ifragCoord = ivec2(gl_FragCoord);
    ivec2 intMouse = ivec2(iMouse.xy);
    
    vec4 draw = texture(iChannel0, uv);
    vec4 kernel = texture(iChannel1, uv);
    
    if (ifragCoord.x == intMouse.x && ifragCoord.y == intMouse.y)  {
        draw = vec4(1,1,1,1);  // white
    } 

    float sum = 0.;
    
    sum += kernel.r;
    sum += kernel.g;
    sum += kernel.b;
    sum += kernel.a;
    
    sum /= 4.;  // try 2.4

    
    fragColor = draw;
    fragColor.r -= sum;  // adds to red channel

}
