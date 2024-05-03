# 坐标转换，赤经赤伟转银经银纬
# 参考链接https://docs.astropy.org/en/stable/coordinates/index.html#id1

from astropy import units as u      #用于单位转换的包
from astropy.coordinates import SkyCoord

'''下面写法有错
ra = "12.12"
dec = "12.12"
source = SkyCoord(ra+" "+dec,frame='icrs',unit=(u.hourangle,u.deg))
x = source.galactic.l.deg
print(x)
y = source.galactic.b.deg
print(y)'''

# 单位是时分秒时这样写，建议参考官方链接
ra = "17 42 29"
dec = "-28 59 18"
source = SkyCoord(ra+" "+dec,frame='icrs',unit=(u.hourangle,u.deg))
print(source.galactic)
x = source.galactic.l
print(x)
y = source.galactic.b
print(y)

# 单位是deg时这样写
a = 12.12
b = 12.12
c=SkyCoord(ra=a*u.degree,dec=b*u.degree,frame='icrs')
print(c)
d=c.galactic
print(d.l,d.b)
print(d.l.deg, d.b.deg)

# 坐标列表时
c = SkyCoord(ra=[10, 11, 12, 13]*u.degree, dec=[41, -5, 42, 0]*u.degree)
for i in c:
    print(i)