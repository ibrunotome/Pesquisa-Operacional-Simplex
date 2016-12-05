var m >= 0;
var s >= 0;
var t >= 0;
var y1 >= 0;
var y2 >= 0;
var y3 >= 0;
var x1 >= 0;
var x2 >= 0;
var x3 >= 0;
var x4 >= 0;
var x5 >= 0;
var x6 >= 0;
var x7 >= 0;

minimize lucro: - 8680 * m - 4140 * s - 82800 * t + 2000000 * y1 + 2000000 * y2 + y3 * 2000000;

subject to 

maxM: m + x1 = 132; 
minM: m - x2 + y1 = 66; 
maxS: s + x3 = 159; 
minS: s - x4 + y2 = 53; 
maxT: t + x5 = 3; 
minT: t - x6 + y3 = 1; 
maxInv: 2860 * m + 3520 * s + 36490 * t + x7 = 1000000;

solve;
display lucro, maxInv, m, s, t, y1, y2, y3,x1, x2, x3, x4, x5, x6, x7;