
import math
import random
import sys
from pwn import *
import json
sys.path.insert(0,'../pwntools')
from pwntools import json_send,json_recv
# from main import get_prime_factors,download_file,decrypt
# download_file('https://cryptohack.org/static/challenges/13386_3d6974846ab20b12c216ff403ec9c99b.py','13386.py')
# Solution based on "Low-Exponent RSA with Related Messages" paper using Groebner Bases
#
# get data from challenge
#
# nc socket.cryptohack.org 13386
# Come back as much as you want! You'll never get my flag.
# { "option":"get_flag" }
# {"encrypted_flag": 4652919307361668525555243060356843281540055910418231362512878965365497240612982130925072925003301104609753179582584737967984468191051663102306686268892551122581935370593210500665076480234520568292365064338296469416453233244976073252070661191008977962558546050674709980772971695390340562617151686825249203642474230197507925248803728702724777355018842870117484624846601013182310739577389688114053195260708343333777364905823730917246866478393530676785983844036784971253354036937277274972539857198327111283196627507066020740764086363737396854787496813662698335117653756755492549059507575855020425741060888637910072269188, "modulus": 17053089605305335736905501318930775061160032133403511203069432150576271780322702147359157180318544661635267433996902331097649035044460468878007551836357610216268485785640470414253753217606761596603894037021963021943370400279879642811495203024600039313504500426573540015974803643423630892006757575890998784236710576745388354316858464035104061710949489910416360431454301778423319148378136826821331373991385616013491010150916643431710769182870846648116676786812005573228313618999700142315465413297050831721461219522200289417912285841565366017214112587852472304779121226893913248687200761678699221403026787511133622521611, "padding": [11180882440749216336388120401800447142860354041308869545635988272297456372987319529916971356321019647413376294599723516471760216919727637625127457630829252974004847096423688574018652640732746011595419739472064842296533619438508600258676872610346555285792409207784404014971999103431919080901834238068567077870789149974761041118012608606899318467020089045363520873062187627795588604626746808624719534889564923832401962168594572494899829247277823790958906925270451999875070467362462140373665903591101331347572863924802086566108340513399749267791465251523590947968193379296123079618505132691540923036455908660188127132010, 14883816822711481338262218131769818348251967300227063152492912895967925064551764925036410310996221615931378777368097212304987975150535258988464407209626516282551622327991343579783633032607532435640720545128193070811921894581263630351484485083807804405685226596764891083124453813267067102254837052657090192102952321638279557405162851801212586969359016633130018166208150418381893002424825481633058772706833088179581356522127160461563819352324098652408325185205599845557811118535478898023980723299101664717675056938989303684117396604854698736669882205064448864365789028705589866712445415526430187589749463237106855727238]}
# { "option":"get_flag" }
# {"encrypted_flag": 5766633922640060801845796553737028648888629553241819200654179316501683841439868571915340158296541976600136227829068559077955933511105218141134012117011297500502725186275344322671631450908192413900969115089751151987899270236380959193760637953741797680657016718869838786925980673424564991982309059811563778586738794022615247615699771839824317464800769272111899666473322160855200692498893654574942411345262414311057198278716859951562886122822560377628284362316836542989303066232964055802645976855334100845538987440261523187858933298963678275174424749197127996820856838477779145445061414854595494213620542582957565388985, "modulus": 17053089605305335736905501318930775061160032133403511203069432150576271780322702147359157180318544661635267433996902331097649035044460468878007551836357610216268485785640470414253753217606761596603894037021963021943370400279879642811495203024600039313504500426573540015974803643423630892006757575890998784236710576745388354316858464035104061710949489910416360431454301778423319148378136826821331373991385616013491010150916643431710769182870846648116676786812005573228313618999700142315465413297050831721461219522200289417912285841565366017214112587852472304779121226893913248687200761678699221403026787511133622521611, "padding": [16926758285869562478573456418346210045398384343725562308601774886839985292088986234316912273890731115351575910719157320408884418841733694750591404064880874498961330602951735135349752754283887264131585679873272449045825055080785344534974888303793100499651782636998800869754654091204237375020459317459242987205685389070686781432411693982710855139353037781722759048841276137168104775899347615424650412155756981330432159793204334245093982950414141936734192587755331255867637689250274150304407804058956214139604599539601929561491966237122815758866326292148348012098491333381656267931150187258942609703815606768874378844559, 874195186508388450815948579499305758258926140515232218538319050304122071351457444017929049073665761766294138900108709952892211858944481880253853791512803202325876417054861735006310576713245991383610258842276669800459256190174878806398638066877615125365738518369152527099286421892416687303343036524476080579736933082074815197657922268337736975521526717345714402058421644509724359227293430890319797616155181536431073747911108135180281620432171422326588406247923848426091977385413492594349008976139677277040863425751140589149602186585273267716707554763075050037121350393359615524003081473794848794965394305955235968865]}
#
# prepare for sage

N=17053089605305335736905501318930775061160032133403511203069432150576271780322702147359157180318544661635267433996902331097649035044460468878007551836357610216268485785640470414253753217606761596603894037021963021943370400279879642811495203024600039313504500426573540015974803643423630892006757575890998784236710576745388354316858464035104061710949489910416360431454301778423319148378136826821331373991385616013491010150916643431710769182870846648116676786812005573228313618999700142315465413297050831721461219522200289417912285841565366017214112587852472304779121226893913248687200761678699221403026787511133622521611
e=11

c1=4652919307361668525555243060356843281540055910418231362512878965365497240612982130925072925003301104609753179582584737967984468191051663102306686268892551122581935370593210500665076480234520568292365064338296469416453233244976073252070661191008977962558546050674709980772971695390340562617151686825249203642474230197507925248803728702724777355018842870117484624846601013182310739577389688114053195260708343333777364905823730917246866478393530676785983844036784971253354036937277274972539857198327111283196627507066020740764086363737396854787496813662698335117653756755492549059507575855020425741060888637910072269188
a1=11180882440749216336388120401800447142860354041308869545635988272297456372987319529916971356321019647413376294599723516471760216919727637625127457630829252974004847096423688574018652640732746011595419739472064842296533619438508600258676872610346555285792409207784404014971999103431919080901834238068567077870789149974761041118012608606899318467020089045363520873062187627795588604626746808624719534889564923832401962168594572494899829247277823790958906925270451999875070467362462140373665903591101331347572863924802086566108340513399749267791465251523590947968193379296123079618505132691540923036455908660188127132010
b1=14883816822711481338262218131769818348251967300227063152492912895967925064551764925036410310996221615931378777368097212304987975150535258988464407209626516282551622327991343579783633032607532435640720545128193070811921894581263630351484485083807804405685226596764891083124453813267067102254837052657090192102952321638279557405162851801212586969359016633130018166208150418381893002424825481633058772706833088179581356522127160461563819352324098652408325185205599845557811118535478898023980723299101664717675056938989303684117396604854698736669882205064448864365789028705589866712445415526430187589749463237106855727238

c2=5766633922640060801845796553737028648888629553241819200654179316501683841439868571915340158296541976600136227829068559077955933511105218141134012117011297500502725186275344322671631450908192413900969115089751151987899270236380959193760637953741797680657016718869838786925980673424564991982309059811563778586738794022615247615699771839824317464800769272111899666473322160855200692498893654574942411345262414311057198278716859951562886122822560377628284362316836542989303066232964055802645976855334100845538987440261523187858933298963678275174424749197127996820856838477779145445061414854595494213620542582957565388985 
a2=16926758285869562478573456418346210045398384343725562308601774886839985292088986234316912273890731115351575910719157320408884418841733694750591404064880874498961330602951735135349752754283887264131585679873272449045825055080785344534974888303793100499651782636998800869754654091204237375020459317459242987205685389070686781432411693982710855139353037781722759048841276137168104775899347615424650412155756981330432159793204334245093982950414141936734192587755331255867637689250274150304407804058956214139604599539601929561491966237122815758866326292148348012098491333381656267931150187258942609703815606768874378844559
b2=874195186508388450815948579499305758258926140515232218538319050304122071351457444017929049073665761766294138900108709952892211858944481880253853791512803202325876417054861735006310576713245991383610258842276669800459256190174878806398638066877615125365738518369152527099286421892416687303343036524476080579736933082074815197657922268337736975521526717345714402058421644509724359227293430890319797616155181536431073747911108135180281620432171422326588406247923848426091977385413492594349008976139677277040863425751140589149602186585273267716707554763075050037121350393359615524003081473794848794965394305955235968865

# Reading Low-Exponent RSA with Related Messages 4.1
# (https://link.springer.com/content/pdf/10.1007/3-540-68339-9_1.pdf)
# Section 4.1 "Arbitrary polynomial relationship among messages"

# Suppose we have k messages m1 .. mk, related by a polynomial p(m1, ..., mk),
# and that we know the ciphertexts ci = mi**e mod N and the coefficients of the
# polynomial p. As before, substitute variables xi, for the unknown messages mi
# and obtain the k + 1 polynomials
#
# P0(x1,..,xk) = p(x1,...,xk) = 0 mod N
#       P1(x1) = x1**e - c1 = 0 mod N
#       P2(x2) = x2**e - c2 = 0 mod N
#       ...
#       Pk(xk) = xk**e - ck = 0 mod N
#
# which must be simultaneously satisfied. We can just compute
#
# Groebner([P0, P1, ..., Pk])
# and generally obtain the answer
#
# [x1 - m1, ..., xk - mk]
# --------------------------------------
# in our case we have same m but different mi (cause of linear transformation)
#
# m1=x1 = a1*m + b1
# m2=x2 = a2*m + b2
#
# which also gives the needed polynomial property  (x1-b1) * a2 == (x2-b2) * a1
#
# so we can write

R.<x1,x2> = PolynomialRing(Zmod(N))
I = R.ideal([(x1-b1)*a2 - (x2-b2)*a1, x1**e - c1, x2**e -c2])
gb = I.groebner_basis()

# to get
# x1 + 3655791390476827588990366376638549482978477765533730171786634398122078929354072167131325256176555456814707431013940717078616676315727738087233391998496401651839315523683014536980209535775222566237791285766075099224408670239488408191965883789734802583212217683426119280056641704925589751211275446555383298122898202178225145919986946019309566448176139971369286716406704897829354114676493506343727362638444714856850328282707488967237135364955803028310974063046348836002838246309569998979099706538652531142888855502616976755218847284424296461654817383763272712375152849350612173933934198516863451538270131303093853285881 
# x2 + 15248867777880535442146152068681888836570795663374038699193401142554168921701705450462650597907845836580834942725714708485936784970497337384251427381603303347238085917459104100374539975109735008315268246565906068482652987289099181829044097629171617138656359068461139402124138442442321462668053348273868801713378273783066228047507117464557898316695985302805855968161987278947380616697031288655783386388677662987310600192251900304525834842066995633457685291750914640529481684600811751091717138401518942893301392881281732064091205629833867665361380869067304994073020601167642040646793426536920270934055910285800428050874
# so 

m1 = N - gb.coefficient_matrix()[0][0][2]
m2 = N - gb.coefficient_matrix()[0][1][2]

# knowing m1 = a1*m + b1 we can compute m

m = (m1-b1) * inverse_mod(a1,N)

# get the flag
hex(int(m))[2:-1].decode("hex")