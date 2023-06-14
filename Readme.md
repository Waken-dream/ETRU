# ETRU Implementation via Python

ETRU is an NTRU-like cryptosystem based on the Eisenstein integers Z[ω] where ω is a primitive cube root of unity. (The NTRU public key cryptosystem was proposed by J. Hoffstein, J. Pipher and J. H. Silverman in 1996. NTRU keys are truncated polynomials with integer coefficients.)

Should have Python 3.x installed on your system.

# Disclaimer

**Under no circumstances should this be used for a cryptographic application!**

This Project is written for a homework to extend NTRU into the Eisenstein Ring.

Guided by paper [ETRU: NTRU over the Eisenstein integers (Monica Nevins)](https://www.researchgate.net/publication/257555334_ETRU_NTRU_over_the_Eisenstein_integers) and [ETRU: NTRU over the Eisenstein integers(Katherine Jarvis · Monica Nevins)](https://link.springer.com/article/10.1007/s10623-013-9850-3)

# What's in this project

```Eisenstein.py```: Definition of Eisenstein Integer and Eisenstein Integer Ring

`EisensteinPloynomial.py`: Definition of Eisenstein Polynomial. Polynomials which coefficients are all Eisenstein Integers.

`classETRU.py`: Definition of ETRU, with method to (1) generate public key & private keys (2) encrypt (3) decrypt

# How to use

At the first time you use this package, delete the file `helper.so` and run the following command in Terminal to compile pybind C++ file `helpers.cpp` and generate a new `helper.so` in your directory.

```bash
(base)% g++ -O3 -Wall -shared -std=c++11 -undefined dynamic_lookup $(python3 -m pybind11 --includes) helpers.cpp -lgmp -o helpers.so
```

Or directly run the `runme.sh` to execute the command above.

Or you can skip the step above by modifying all the helpers usage. For example modify the `is_prime()` method in `Eisenstein.py` to avoid use helpers.so

```python
@property
    def is_prime(self):
        '''
        Proposition 4.2.4: If φ ∈ Z[ω] and d (φ) = p where p is a rational prime, then φ is a prime in Z[ω].
        :return: bool: True or False
        '''
        if is_prime(self.norm):
        #if helpers.is_prime(self.norm):
            return True
        else:
            return False
```

## Key Generation

To generate random public and private key pair execute:

```shell
(base)% python etru.py gen key_priv key_pub
(0 + 1*omega)x^244 + (1 + 0*omega)x^243 + (-1 + 0*omega)x^242 + (0 + 1*omega)x^241 + (0 + 1*omega)x^240 + (1 + 1*omega)x^239 + (1 + 1*omega)x^237 + (-1 + 0*omega)x^236 + (1 + 0*omega)x^235 + (-1 + -1*omega)x^233 + (-1 + -1*omega)x^232 + (-1 + -1*omega)x^231 + (0 + 1*omega)x^230 + (1 + 1*omega)x^228 + (0 + -1*omega)x^227 + (1 + 0*omega)x^226 + (1 + 0*omega)x^225 + (0 + 1*omega)x^224 + (1 + 1*omega)x^223 + (-1 + 0*omega)x^222 + (1 + 0*omega)x^221 + (-1 + -1*omega)x^220 + (-1 + -1*omega)x^219 + (0 + -1*omega)x^217 + (1 + 0*omega)x^216 + (-1 + 0*omega)x^215 + (0 + -1*omega)x^214 + (-1 + 0*omega)x^213 + (-1 + 0*omega)x^212 + (0 + 1*omega)x^211 + (1 + 0*omega)x^209 + (-1 + -1*omega)x^208 + (0 + 1*omega)x^206 + (1 + 0*omega)x^205 + (-1 + -1*omega)x^204 + (1 + 0*omega)x^202 + (1 + 1*omega)x^201 + (1 + 0*omega)x^200 + (0 + 1*omega)x^199 + (0 + 1*omega)x^198 + (1 + 1*omega)x^197 + (-1 + -1*omega)x^196 + (1 + 0*omega)x^195 + (-1 + 0*omega)x^194 + (1 + 1*omega)x^193 + (1 + 0*omega)x^192 + (0 + -1*omega)x^191 + (1 + 0*omega)x^188 + (1 + 0*omega)x^185 + (1 + 0*omega)x^184 + (1 + 1*omega)x^183 + (-1 + -1*omega)x^182 + (0 + -1*omega)x^181 + (-1 + 0*omega)x^180 + (0 + 1*omega)x^178 + (-1 + -1*omega)x^177 + (0 + -1*omega)x^175 + (1 + 0*omega)x^174 + (1 + 1*omega)x^172 + (0 + -1*omega)x^171 + (1 + 0*omega)x^170 + (0 + 1*omega)x^169 + (0 + 1*omega)x^168 + (0 + -1*omega)x^167 + (0 + -1*omega)x^166 + (0 + 1*omega)x^165 + (0 + 1*omega)x^164 + (-1 + -1*omega)x^163 + (1 + 1*omega)x^162 + (1 + 1*omega)x^161 + (1 + 1*omega)x^160 + (-1 + 0*omega)x^157 + (1 + 1*omega)x^156 + (0 + -1*omega)x^155 + (1 + 0*omega)x^154 + (1 + 0*omega)x^153 + (1 + 0*omega)x^152 + (-1 + 0*omega)x^151 + (1 + 1*omega)x^150 + (-1 + 0*omega)x^149 + (-1 + 0*omega)x^148 + (1 + 1*omega)x^147 + (1 + 1*omega)x^146 + (-1 + -1*omega)x^144 + (1 + 1*omega)x^143 + (0 + 1*omega)x^142 + (0 + -1*omega)x^141 + (-1 + -1*omega)x^140 + (1 + 1*omega)x^139 + (-1 + -1*omega)x^138 + (0 + 1*omega)x^137 + (0 + 1*omega)x^136 + (-1 + 0*omega)x^135 + (1 + 1*omega)x^134 + (-1 + -1*omega)x^132 + (1 + 0*omega)x^131 + (0 + -1*omega)x^130 + (0 + 1*omega)x^126 + (-1 + -1*omega)x^125 + (-1 + 0*omega)x^124 + (0 + -1*omega)x^123 + (0 + -1*omega)x^122 + (1 + 1*omega)x^121 + (1 + 1*omega)x^120 + (-1 + -1*omega)x^119 + (-1 + -1*omega)x^118 + (-1 + 0*omega)x^117 + (-1 + -1*omega)x^116 + (-1 + -1*omega)x^115 + (1 + 1*omega)x^114 + (0 + 1*omega)x^113 + (-1 + 0*omega)x^112 + (0 + 1*omega)x^111 + (0 + 1*omega)x^109 + (0 + -1*omega)x^108 + (-1 + 0*omega)x^107 + (-1 + -1*omega)x^106 + (-1 + 0*omega)x^105 + (-1 + 0*omega)x^104 + (-1 + 0*omega)x^103 + (0 + -1*omega)x^101 + (1 + 0*omega)x^99 + (0 + 1*omega)x^98 + (-1 + 0*omega)x^97 + (-1 + -1*omega)x^96 + (1 + 1*omega)x^95 + (0 + 1*omega)x^94 + (0 + -1*omega)x^93 + (1 + 0*omega)x^92 + (-1 + -1*omega)x^91 + (1 + 0*omega)x^90 + (0 + -1*omega)x^89 + (-1 + -1*omega)x^88 + (0 + 1*omega)x^87 + (0 + -1*omega)x^86 + (0 + -1*omega)x^85 + (-1 + 0*omega)x^84 + (-1 + 0*omega)x^83 + (0 + -1*omega)x^82 + (-1 + 0*omega)x^81 + (0 + -1*omega)x^80 + (-1 + 0*omega)x^79 + (1 + 1*omega)x^78 + (-1 + 0*omega)x^77 + (1 + 1*omega)x^76 + (1 + 0*omega)x^75 + (0 + -1*omega)x^73 + (0 + 1*omega)x^72 + (1 + 1*omega)x^71 + (1 + 1*omega)x^70 + (0 + 1*omega)x^69 + (-1 + 0*omega)x^68 + (0 + 1*omega)x^65 + (0 + -1*omega)x^64 + (0 + 1*omega)x^63 + (0 + 1*omega)x^62 + (0 + -1*omega)x^61 + (-1 + -1*omega)x^60 + (-1 + 0*omega)x^59 + (-1 + -1*omega)x^57 + (-1 + 0*omega)x^55 + (1 + 0*omega)x^53 + (0 + 1*omega)x^51 + (1 + 0*omega)x^50 + (-1 + -1*omega)x^49 + (1 + 1*omega)x^48 + (-1 + -1*omega)x^47 + (0 + 1*omega)x^46 + (-1 + 0*omega)x^45 + (1 + 1*omega)x^44 + (-1 + 0*omega)x^42 + (1 + 1*omega)x^41 + (0 + -1*omega)x^40 + (0 + -1*omega)x^39 + (0 + 1*omega)x^38 + (1 + 0*omega)x^37 + (-1 + -1*omega)x^36 + (0 + -1*omega)x^35 + (1 + 1*omega)x^34 + (0 + 1*omega)x^33 + (-1 + -1*omega)x^32 + (1 + 1*omega)x^31 + (0 + -1*omega)x^30 + (1 + 0*omega)x^29 + (-1 + -1*omega)x^28 + (1 + 0*omega)x^27 + (0 + 1*omega)x^26 + (1 + 1*omega)x^25 + (-1 + -1*omega)x^24 + (0 + 1*omega)x^23 + (1 + 0*omega)x^22 + (1 + 0*omega)x^21 + (0 + -1*omega)x^20 + (0 + -1*omega)x^19 + (0 + -1*omega)x^18 + (0 + -1*omega)x^17 + (-1 + -1*omega)x^16 + (0 + -1*omega)x^15 + (1 + 0*omega)x^14 + (1 + 1*omega)x^13 + (1 + 0*omega)x^12 + (-1 + 0*omega)x^10 + (-1 + -1*omega)x^9 + (0 + -1*omega)x^8 + (1 + 0*omega)x^7 + (-1 + -1*omega)x^6 + (-1 + 0*omega)x^4 + (1 + 0*omega)x^3 + (1 + 1*omega)x^2 + (-1 + 0*omega)x^1 + (-1 + 0*omega)
```

Attention: $N,\ p,\ q$ should not be changed arbitrarily, input strings are encode into domain $R_p$. In this program, $p$ is set to be Eisenstein prime $2+3\omega$ so that $R_p=\{ 0,\pm1,\pm\omega,\pm\omega^2 \}$, $q$ is set to be $167\omega$ far bigger than $p$ to prevent decryption failure.

If you really want to change the value of $N,\ p,\ q$, modify the `eisenstein_encode` and `eisenstein_decode` function in `utils.py` accordingly. Larger $p$ can reduce the degree of message polynomial.

The `key_priv.npz` and `key_pub.npz` files should appear in current working directory. These are zip compressed NumPy files which contains:

* both keys:
  * N (default = 251)
  * p (default = $2+3\omega$)
  * q (default = $167\omega$)
* private key:
  * f
  * f_p
  * g (Debug mode only)
  * f_q (Debug mode only)
* public key:
  * h

## Encrypt

Use the standard input and output, run the following command in Terminal.

```shell
(base)%  echo "I am Maozihao" | python etru.py enc key_pub.npz
￪E￠%.ﾱ￾V
￷ﾭﾷﾻ ￧=￶ﾪ￝ￍﾯﾬ'￧￪ￔ￮ﾨ9JHTￎﾔﾣￂﾬ￺￢￬!&ﾲￅ%*￲￠ￋ561%E:j8�ￛ￳'￫￢9ￍ-fl4￺
                                                                ￥ﾱﾾￎﾳﾢﾼ3
                                                                         >￨1ￖ16￨￺ﾳￎﾸﾠﾽﾾﾻJﾹ￶￨￣
                                                                                              ',(<A￥X3ﾻ￬￴￉NQ
￵￱ﾳￚﾲ￠a￸￺ﾣ￨ﾾ￰￦ￎ[!ﾭﾮa;ￔ=￩ﾰￅRﾼ￈ ￬-ￇ7�BW"ￎ￿F
        Aￍﾢ2#ￂￋￇﾩ￡￿ￌ￉ￖ￲ￆﾸ￡$B￤ﾤ8￙>4F￨ￓA￢ￄ￣ﾫ￥ﾮ￮
                                                   ﾷ?*>￝￡]3:￳ￚￌￆￒ￷ﾭZ?ﾸ
￀ￇ$>ￅ0J<￪!﾿ￕD                                                          -=￴￻￫ￋ￹￲0￸ￕ￫ￍ<ￛﾻ>￵%
￀(￭ﾱﾭ￨GYￖ￺￡ￌ￘￁￺ﾪ￧(￹ﾶ￴ￌ=X￳ￎ/￞!L
                               ￷ￔￂ￪     ￩￭￣ﾭQ￿￺)]6I1ￊﾩ￫8￿$ￏￏ1￨￡ﾻￏ￴￨ﾪￊￏ ?HI￘ﾟB￺￟!￥ﾾﾴﾼ7￫]"￾￉'I%￢ﾶ￡￪EBﾰￖ￰￯ﾻ￤
ￆ￤6,Pﾷￅ￡ﾴ￻￣￺/￦!ￒ+,!￉Y>￳ (   ￝ﾴ￭ￄ￨%ﾻ"￬>ￊ￣1￥.￲Eﾺ￨ERH￦ﾸ>[%
```

This encrypt the string `"I am Maozihao"`. Or you can set the polynomial output by entering the command below to gain a polynomial output.

```shell
(base)% echo "I am Maozihao" | python etru.py -o enc key_pub.npz
(31 + 98*omega)x^250 + (71 + 45*omega)x^249 + (38 + 46*omega)x^248 + (-50 + 19*omega)x^247 + (12 + -51*omega)x^246 + (52 + 72*omega)x^245 + (21 + 76*omega)x^244 + (-14 + 28*omega)x^243 + (76 + 8*omega)x^242 + (90 + 31*omega)x^241 + (-62 + -72*omega)x^240 + (51 + 43*omega)x^239 + (-5 + -69*omega)x^238 + (-63 + 3*omega)x^237 + (8 + 37*omega)x^236 + (-61 + 37*omega)x^235 + (52 + -10*omega)x^234 + (96 + 50*omega)x^233 + (-12 + -50*omega)x^232 + (32 + 61*omega)x^231 + (-51 + -37*omega)x^230 + (-86 + -64*omega)x^229 + (0 + -47*omega)x^228 + (2 + 47*omega)x^227 + (47 + 62*omega)x^226 + (22 + 25*omega)x^225 + (-87 + -47*omega)x^224 + (26 + 51*omega)x^223 + (76 + -8*omega)x^222 + (-86 + -55*omega)x^221 + (-31 + 27*omega)x^220 + (-56 + -78*omega)x^219 + (22 + 91*omega)x^218 + (59 + -48*omega)x^217 + (-83 + 1*omega)x^216 + (11 + 13*omega)x^215 + (33 + 41*omega)x^214 + (28 + 69*omega)x^213 + (54 + 93*omega)x^212 + (63 + 90*omega)x^211 + (60 + 71*omega)x^210 + (-9 + -50*omega)x^209 + (-86 + -66*omega)x^208 + (-44 + -5*omega)x^207 + (-18 + -73*omega)x^206 + (66 + 69*omega)x^205 + (-77 + -8*omega)x^204 + (-27 + -93*omega)x^203 + (21 + 82*omega)x^202 + (-75 + -59*omega)x^201 + (47 + -8*omega)x^200 + (12 + 12*omega)x^199 + (-17 + 60*omega)x^198 + (6 + -8*omega)x^197 + (-32 + -22*omega)x^196 + (-13 + -68*omega)x^195 + (3 + 46*omega)x^194 + (43 + 22*omega)x^193 + (-18 + 32*omega)x^192 + (35 + 14*omega)x^191 + (32 + 99*omega)x^190 + (69 + 91*omega)x^189 + (-60 + 18*omega)x^188 + (-63 + -52*omega)x^187 + (36 + 19*omega)x^186 + (-51 + -67*omega)x^185 + (-23 + 68*omega)x^184 + (-44 + 42*omega)x^183 + (55 + -4*omega)x^182 + (-46 + -15*omega)x^181 + (100 + 49*omega)x^180 + (74 + 17*omega)x^179 + (-9 + 7*omega)x^178 + (15 + 84*omega)x^177 + (-19 + 55*omega)x^176 + (-19 + -78*omega)x^175 + (-95 + -46*omega)x^174 + (-77 + -61*omega)x^173 + (-56 + -90*omega)x^172 + (-69 + -40*omega)x^171 + (43 + -56*omega)x^170 + (24 + 34*omega)x^169 + (72 + 46*omega)x^168 + (-6 + -27*omega)x^167 + (-46 + -46*omega)x^166 + (92 + 75*omega)x^165 + (-5 + 27*omega)x^164 + (47 + 74*omega)x^163 + (-70 + -7*omega)x^162 + (-53 + 51*omega)x^161 + (41 + 71*omega)x^160 + (-50 + -88*omega)x^159 + (-91 + -67*omega)x^158 + (24 + 31*omega)x^157 + (37 + -14*omega)x^156 + (15 + -65*omega)x^155 + (9 + 38*omega)x^154 + (-18 + -8*omega)x^153 + (-12 + -26*omega)x^152 + (70 + 22*omega)x^151 + (-58 + -17*omega)x^150 + (42 + 3*omega)x^149 + (-83 + -71*omega)x^148 + (31 + -63*omega)x^147 + (34 + 37*omega)x^146 + (66 + 48*omega)x^145 + (-28 + 43*omega)x^144 + (42 + -55*omega)x^143 + (-39 + -89*omega)x^142 + (81 + 81*omega)x^141 + (75 + 57*omega)x^140 + (48 + -45*omega)x^139 + (39 + 52*omega)x^138 + (61 + 1*omega)x^137 + (83 + 32*omega)x^136 + (45 + 40*omega)x^135 + (28 + 70*omega)x^134 + (69 + 87*omega)x^133 + (-7 + -76*omega)x^132 + (2 + -40*omega)x^131 + (-18 + -6*omega)x^130 + (45 + 70*omega)x^129 + (59 + 108*omega)x^128 + (40 + 21*omega)x^127 + (62 + 6*omega)x^126 + (89 + 18*omega)x^125 + (70 + 57*omega)x^124 + (-18 + -6*omega)x^123 + (-56 + -103*omega)x^122 + (57 + 26*omega)x^121 + (46 + 21*omega)x^120 + (23 + -21*omega)x^119 + (36 + -55*omega)x^118 + (-20 + -38*omega)x^117 + (-71 + 17*omega)x^116 + (23 + 63*omega)x^115 + (3 + -75*omega)x^114 + (-47 + 37*omega)x^113 + (29 + 69*omega)x^112 + (-56 + -58*omega)x^111 + (24 + 92*omega)x^110 + (33 + -29*omega)x^109 + (-59 + 47*omega)x^108 + (-54 + -26*omega)x^107 + (-72 + 17*omega)x^106 + (-8 + -84*omega)x^105 + (-33 + -82*omega)x^104 + (-65 + 37*omega)x^103 + (48 + -14*omega)x^102 + (65 + 102*omega)x^101 + (-1 + 58*omega)x^100 + (-30 + -45*omega)x^99 + (49 + -53*omega)x^98 + (14 + 67*omega)x^97 + (-57 + -31*omega)x^96 + (-19 + -55*omega)x^95 + (51 + -5*omega)x^94 + (10 + 70*omega)x^93 + (-67 + -11*omega)x^92 + (-4 + 39*omega)x^91 + (4 + -38*omega)x^90 + (67 + 61*omega)x^89 + (9 + -42*omega)x^88 + (39 + 72*omega)x^87 + (52 + 40*omega)x^86 + (10 + 16*omega)x^85 + (-1 + -77*omega)x^84 + (-62 + -70*omega)x^83 + (29 + -56*omega)x^82 + (14 + 13*omega)x^81 + (-58 + 48*omega)x^80 + (-9 + -33*omega)x^79 + (18 + -1*omega)x^78 + (58 + 38*omega)x^77 + (47 + 64*omega)x^76 + (19 + -2*omega)x^75 + (57 + 58*omega)x^74 + (17 + 22*omega)x^73 + (-16 + -86*omega)x^72 + (-41 + 14*omega)x^71 + (37 + -19*omega)x^70 + (42 + -61*omega)x^69 + (7 + -31*omega)x^68 + (25 + -43*omega)x^67 + (42 + -51*omega)x^66 + (-10 + 19*omega)x^65 + (73 + 11*omega)x^64 + (65 + 78*omega)x^63 + (55 + -9*omega)x^62 + (-68 + 8*omega)x^61 + (43 + 94*omega)x^60 + (8 + -20*omega)x^59 + (-20 + 27*omega)x^58 + (42 + 11*omega)x^57 + (73 + 10*omega)x^56 + (-16 + 2*omega)x^55 + (-32 + -75*omega)x^54 + (56 + -28*omega)x^53 + (7 + -44*omega)x^52 + (-73 + -91*omega)x^51 + (-23 + -55*omega)x^50 + (83 + 53*omega)x^49 + (44 + 59*omega)x^48 + (12 + 20*omega)x^47 + (8 + -64*omega)x^46 + (-59 + 43*omega)x^45 + (-73 + -38*omega)x^44 + (-26 + -57*omega)x^43 + (-35 + 3*omega)x^42 + (-63 + 33*omega)x^41 + (8 + 79*omega)x^40 + (-44 + 32*omega)x^39 + (8 + -3*omega)x^38 + (5 + 52*omega)x^37 + (76 + 6*omega)x^36 + (-55 + -41*omega)x^35 + (-74 + -62*omega)x^34 + (2 + -33*omega)x^33 + (90 + 57*omega)x^32 + (47 + 61*omega)x^31 + (75 + 45*omega)x^30 + (76 + 79*omega)x^29 + (-108 + -58*omega)x^28 + (-59 + -6*omega)x^27 + (96 + 60*omega)x^26 + (-15 + -69*omega)x^25 + (-8 + 35*omega)x^24 + (-61 + 33*omega)x^23 + (-4 + 65*omega)x^22 + (-19 + -6*omega)x^21 + (-16 + -43*omega)x^20 + (14 + -66*omega)x^19 + (24 + -54*omega)x^18 + (-34 + -97*omega)x^17 + (41 + -50*omega)x^16 + (-100 + -40*omega)x^15 + (2 + -33*omega)x^14 + (-36 + 17*omega)x^13 + (77 + 58*omega)x^12 + (17 + 47*omega)x^11 + (-41 + -68*omega)x^10 + (25 + 91*omega)x^9 + (-103 + -39*omega)x^8 + (-24 + 35*omega)x^7 + (69 + 42*omega)x^6 + (-66 + -56*omega)x^5 + (-100 + -59*omega)x^4 + (-5 + 64*omega)x^3 + (2 + 81*omega)x^2 + (-54 + 39*omega)x^1 + (75 + 70*omega)
```

You can also use file input and redirect the output to a txt file by using the command below.

```shell
(base)% python etru.py enc key_pub.npz plaintext.txt > ciphertext.txt
```

## Decrypt

First let me show you the cipher text.

```shell
(base)% cat ciphertext.txt
P�￵￀￰￣￣ￚF￤ﾨ
ﾸ￭￥"￵:ﾸ'U;H￸ￋￎ.ￔ;DH￘￯￞ﾸ￳ￊﾼ￤￰ﾯ￙￩ￓ￦ﾪ￥6
                                        @@ￃￇJ]=j￰￝￀￲:￫ﾺ￺ﾪ￵￟￹$ﾬￍ￙ﾠ%\ﾬ￴￉
                                                                      ﾨￋ￧ﾤ"M&ﾼ￫ￗY0GE￟￬ﾱ￦ￜ￩ﾩ0"￮ﾳeA￼ﾳﾰﾱ￙ﾠ$ￊAﾪￚM3Q Eￆ￉J
￼￑￮ￖ!ﾭ￤9cJ?￶NJ(:@/￁￵\ﾰￂ%￩=D￷ﾵ￘￦C￠9`￉￮ﾹﾭ￳ￕ                                                                         ￦ﾪￛﾛￂￍﾞￆ"￧D￡#
SI(￑2Nￛ￼>ￚﾬ￧ﾽ￞￧﾿ￛ0[F4B5=￪￈￝￉￠ﾼ￮￳￝$ￊﾳﾶﾯ;￶ﾽ￺M&ﾼￔ￧,ﾻﾽI$ￖﾯT;ￕ￨6M?￧ﾳ￧ﾨ￷￀￁ￜ,ￒﾥ￭￬￠ﾫ"￀￠￝￮�ﾚￍ
                                                                                       0        %bￕﾳ￬ﾱﾱﾰﾵﾴￒ￨￠ￜﾷ61)ￔﾢ*e(*ﾽ￤￩8￲Iﾻ￸￢ﾰ￨￑5￣￑ﾜL.ￊﾧ%
```

Decrypt is used similar as encrypt. You can use the command below to decrypt the cipher text in `ciphertext.txt`

```shell
(base)% cat ciphertext.txt | python etru.py dec key_priv.npz
-----------------------------
Maozihao
```

## Input size

If the input you provided is too large, the program will return this error.

```shell
Traceback (most recent call last):
  File "/Users/maozihao/Documents/ETRU/etru.py", line 187, in <module>
    output = decrypt(args['PRIV_KEY_FILE'], input_arr, block=block)
  File "/Users/maozihao/Documents/ETRU/etru.py", line 92, in decrypt
    raise OverflowError("Input is too large for current N")
OverflowError: Input is too large for current N
```

In this case, you can use the block mode, which splits the input into blocks of the requested size. Make sure you are using this mode in both encrypting and decrypting process.
