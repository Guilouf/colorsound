#version 330 core
/*
Image buffer
Takes previous image and kernel as input,
returns a new image
*/

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{  
	vec2 uv = fragCoord.xy / iResolution.xy;
    ivec2 ifragCoord = ivec2(fragCoord);
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
