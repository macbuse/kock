#Inkscape extension to make Apollonian gaskets. Tested Inkscape 0.91.

The Koch snowflake  is a mathematical curve and one of the earliest fractal curves to have been described.
It is based on the Koch curve, which appeared in a 1904 paper titled "On a continuous curve without tangents, constructible from elementary geometry" (original French title: Sur une courbe continue sans tangente, obtenue par une construction géométrique élémentaire)[citation needed] by the Swedish mathematician Helge von Koch.
The progression for the area of the snowflake converges to 8/5 times the area of the original triangle,
while the progression for the snowflake's perimeter diverges to infinity.
Consequently, the snowflake has a finite area bounded by an infinitely long line.
 
Source: Wikipedia

##Example Inkscape file

(example Inkscape file)[https://github.com/macbuse/kock/blob/master/koch.svg]

##Installation

1. Edit the first line of koch.inx to point to your python installation if you don't use Anaconda on OSX.
1. Copy the .inx and all the .py to inkscape extensions folder : For OS X - $HOME/.config/inkscape/extensions
1.Open Inkscape.
1. Activate via the Render submenu of Extensions menu.


##Dependencies

Needs Anaconda python on OS X but should work with any python 2.7* installation after modifying as per installation instructions.

##Notes

None
