#version 330 core
/*
Image buffer
Takes previous image and kernel as input,
returns a new image
*/
uniform vec2 iMouse;
uniform int iMouseLeftDown;
uniform int iMouseRightDown;
uniform vec2 iResolution;
uniform sampler2D kernelTexture;
uniform sampler2D iChannel1;
out vec2 fragColor;

void main()
{  
	vec2 uv = gl_FragCoord.xy / iResolution.xy;
    ivec2 ifragCoord = ivec2(gl_FragCoord);
    ivec2 intMouse = ivec2(iMouse.xy);
    
    vec4 kernel = texture(kernelTexture, uv);
    vec2 draw = texture(iChannel1, uv).rg;  // texture only return float or vec4
    
    if (ifragCoord.x == intMouse.x && ifragCoord.y == iResolution.y - intMouse.y
        && iMouseLeftDown == 1)  {
        draw = vec2(1.,1.);  // white
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
