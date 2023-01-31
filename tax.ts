import {intputType} from "./types";

var skatteorakel = false;
// Kan først anvendes fra indkomståret 2004
const indkomstaar = 23;

// indkomstårsafhængige konstanter

const AMBATPprc23 = 8.0; // (8% + 0%) 2023

const bundskatprc23 = 12.09; // 2023

const sundhedsbidragprc23 = 0; // 2023

const topskatprc23 = 15.0; // 2023

const topskatgraense23 = 568900; // 2023

const skatteloftprc23 = 52.07; // 2023

const skatteloftprc_positivkapitalindkomst23 = 42; // 2023

const personfradragUnge23 = 38400; // 2023

const personfradrag23 = 48000; // 2023

const maksimumKapitalpensionsfradrag23 = 0; // 2023

const bundfradrag_positiv_nettokapitalindkomst_konstant = 48800; // 2023

const underAktieskatprc = 27.0; // 2023
const overAktieskatprc = 42.0; // 2023

const aktieskatgrundbeloeb23 = 58900; // 2023

const bundgraenseLoenmodtagerfradrag23 = 6700; // 2023

const maksimumBeskaeftigelsesfradrag23 = 45600; // 2023 (midlertidigt forhoejet i 2022/2023
const beskaeftigelsesfradragsprocent23 = 0.1065; // 2023, jf. LL § 9 J, stk. 2

const bundgraense_jobfradrag = 208700; // 2023
const jobfradragsprocent = 0.045; // 2023
const maksimalt_jobfradrag = 2700; // 2023, jf. LL § 9 K, stk. 2

const nedslagNegativNettokapitalindkomstprc23 = 8.0; // 2023, jf. PSL § 11, stk. 2

const maksimaltEkstraPensionsfradrag = 77900 ; // 2023, jf. LL § 9 L
const ekstraPensionsfradragprocent15aarEllerMindre = 0.32 // 2023, jf. LL § 9 L, stk. 2
const ekstraPensionsfradragprocent1MereEnd5aar = 0.12 // 2023, jf. LL § 9 L, stk. 2

if (indkomstaar == 23) {
	var AMBprc = AMBATPprc23
	var bundskatprc = bundskatprc23
	var sundhedsbidragprc = sundhedsbidragprc23
	var topskatprc = topskatprc23
	var topskatgraense = topskatgraense23
	var skatteloftprc = skatteloftprc23
	var skatteloftprc_positivkapitalindkomst=skatteloftprc_positivkapitalindkomst23
	var personfradragUnge = personfradragUnge23
	var personfradrag = personfradrag23

	var maksimumKapitalpensionsfradrag = maksimumKapitalpensionsfradrag23

	var maksimumBeskaeftigelsesfradrag = maksimumBeskaeftigelsesfradrag23

	var aktieskatgrundbeloeb = aktieskatgrundbeloeb23


	var bundgraenseLoenmodtagerfradrag = bundgraenseLoenmodtagerfradrag23
	var beskaeftigelsesfradragsprocent = beskaeftigelsesfradragsprocent23

	var nedslagNegativNettokapitalindkomstprc = nedslagNegativNettokapitalindkomstprc23
}


const ejendomsvaerdigraense = 3040000 // reguleres ikke fra og med 2002
const ejendomsvaerdiskatprcUnder = 0.92 // 01 - identisk 02/03/04/05/06/07/08/09 2021/22/23: 0,92%
const ejendomsvaerdiskatprcOver = 3 // 01 - identisk 02/03/04/05/06/07/08/09

// variabler der kun bruges ved skatteberegning
var kommunenavn = "ingen"
var kommuneprc = 0
var kirkeprc = 0
var grundskyldpromille = 0
var grundskyldpromilleSommerhus = 0

// variabler der både bruges ved indkomstopgørelse og skatteberegning
var MloenFoerAMB = 0
var KloenFoerAMB = 0

var MAMB = 0 // arbejdsmarkedsbidrag skatteyder
var KAMB = 0 // arbejdsmarkedsbidrag ægtefælle

let MpersonligIndkomst = 0
let MindskudKapitalpension = 0
let MarbejdsgiverIndskudKapitalpension = 0
let Mkapitalindkomst = 0
let MligningsmaessigeFradrag = 0
let MskattepligtigIndkomst = 0
let Maktieindkomst = 0

let KpersonligIndkomst = 0
let KindskudKapitalpension = 0
let KarbejdsgiverIndskudKapitalpension = 0
let Kkapitalindkomst = 0
let KligningsmaessigeFradrag = 0
let KskattepligtigIndkomst = 0
let Kaktieindkomst = 0

// globale, da de skal overføres som globale
var Mtopskat
var skatIalt

var fatalFejl = false // angiver om der er en fejl, som betyder at SkatteOrakel bør undlade at give resultat

function indkomstopgoerelse(form: intputType) {
	// omregning af personlig indkomst før AMB til efter AMB
	let MloenFoerAMB = parse(form.MloenFoerAMB1)
	let KloenFoerAMB = parse(form.KloenFoerAMB1)

	let MAMB = MloenFoerAMB * AMBprc / 100
	let KAMB = KloenFoerAMB * AMBprc / 100

	form.MAMB1 = afrund(MAMB)
	form.KAMB1 = afrund(KAMB)

	let Mloen = MloenFoerAMB - MAMB
	let Kloen = KloenFoerAMB - KAMB

	// Start: regn ud, om skatteyders indskud på kapitalpension overstiger maksimumgrænse
	// Er det tilfældet nedsættes indskudet på privattegnet kapitalpension
	// - og medregnes ikke ved beregning af topskat - da heller ikke bortseelsesret for arbejdsgiveradministreret ordning
	MindskudKapitalpension = parse(form.Mkapital)

	MarbejdsgiverIndskudKapitalpension = parse(form.MarbejdsgiverIndskudKapitalpension)

	let overskridelse = (MindskudKapitalpension + MarbejdsgiverIndskudKapitalpension)
			- maksimumKapitalpensionsfradrag
	if (overskridelse > 0) {
		console.error("Der kan maksimalt fradrages " + tilDanskHeltal(maksimumKapitalpensionsfradrag) + " kr. ved indbetaling på kapitalpensioner!")

		if (MindskudKapitalpension > overskridelse) {
			var MfradragsberettigetIndskudKapitalpension = MindskudKapitalpension - overskridelse
		} else {
			var MfradragsberettigetIndskudKapitalpension = 0
		}

		form.Mkapital = MfradragsberettigetIndskudKapitalpension
	} else {
		MfradragsberettigetIndskudKapitalpension = MindskudKapitalpension
	}

	// Det overskydende beløb medregnes ikke ved beregning af topskat, jfr. personskatteloven § 7, stk. 1
	MindskudKapitalpension = MfradragsberettigetIndskudKapitalpension
	// Slut: regn ud, om indskud på kapitalpension overstiger maksimumgrænse

	// personlig indkomst
	MpersonligIndkomst =
		Mloen 
		+ parse(form.MandenPersonlig)
		- MfradragsberettigetIndskudKapitalpension
		- parse(form.Mrate)

	form.MpersonligIndkomst = afrund(MpersonligIndkomst)

	// Start: regn ud, om ægtefælles indskud på kapitalpension overstiger maksimumgrænse
	// Er det tilfældet nedsættes indskudet på privattegnet kapitalpension
	// - og medregnes ikke ved beregning af topskat - da heller ikke bortseelsesret for arbejdsgiveradministreret ordning
	KindskudKapitalpension = parse(form.Kkapital)
	KarbejdsgiverIndskudKapitalpension = parse(form.KarbejdsgiverIndskudKapitalpension)										

	overskridelse = (KindskudKapitalpension + KarbejdsgiverIndskudKapitalpension)
			- maksimumKapitalpensionsfradrag
	if (overskridelse > 0) {
		console.error("Der kan maksimalt fradrages " + tilDanskHeltal(maksimumKapitalpensionsfradrag) + " kr. ved indbetaling på kapitalpensioner!")

		if (KindskudKapitalpension > overskridelse) {
			var KfradragsberettigetIndskudKapitalpension = KindskudKapitalpension - overskridelse
		} else {
			var KfradragsberettigetIndskudKapitalpension = 0
		}

		form.Kkapital = KfradragsberettigetIndskudKapitalpension
	} else {
		KfradragsberettigetIndskudKapitalpension = KindskudKapitalpension
	}

	// Det overskydende beløb medregnes ikke ved beregning af topskat, jfr. personskatteloven § 7, stk. 1
	KindskudKapitalpension = KfradragsberettigetIndskudKapitalpension
	// Slut: regn ud, om indskud på kapitalpension overstiger maksimumgrænse

	KpersonligIndkomst =
		Kloen 
		+ parse(form.KandenPersonlig)
		- KfradragsberettigetIndskudKapitalpension
		- parse(form.Krate)

	form.KpersonligIndkomst = afrund(KpersonligIndkomst)

	// kapitalindkomst
	Mkapitalindkomst =
		parse(form.Mrenteind)
		+ parse(form.MandenKapital)
		- parse(form.Mrenteud)

	form.Mkapitalindkomst = tilDanskHeltal(afrund(Mkapitalindkomst))

	Kkapitalindkomst =
		parse(form.Krenteind)
		+ parse(form.KandenKapital)
		- parse(form.Krenteud)

	form.Kkapitalindkomst = tilDanskHeltal(afrund(Kkapitalindkomst))

	// ligningsmæssige fradrag

	// Opgørelse af beskæftigelsesfradrag (fra indkomståret 2004)
	// Jfr. lov nr. 442 af 10. juni 2003

	// Ændret 17/12-2020 fra : Mbeskaeftigelsesfradragsgrundlag = Math.max(0,parse(form.MloenFoerAMB1)-parse(form.Mkapital)-parse(form.Mrate))

	var Mbeskaeftigelsesfradragsgrundlag = Math.max(0,parse(form.MloenFoerAMB1)+parse(form.MrateArbejdsgiveradm)) // 2/5-2021
	var Mbeskaeftigelsesfradrag = Math.min(Mbeskaeftigelsesfradragsgrundlag * beskaeftigelsesfradragsprocent,maksimumBeskaeftigelsesfradrag)

	form.Mbeskaeftigelsesfradrag = tilDanskHeltal(afrund(Mbeskaeftigelsesfradrag))

	// Ændret 17/12-2020 fra : Kbeskaeftigelsesfradragsgrundlag = Math.max(0,parse(form.KloenFoerAMB1)-parse(form.Kkapital)-parse(form.Krate))

	var Kbeskaeftigelsesfradragsgrundlag = Math.max(0,parse(form.KloenFoerAMB1)+parse(form.KrateArbejdsgiveradm)) // 2/5-2021
	var Kbeskaeftigelsesfradrag = Math.min(Kbeskaeftigelsesfradragsgrundlag * beskaeftigelsesfradragsprocent,maksimumBeskaeftigelsesfradrag)

	form.Kbeskaeftigelsesfradrag = tilDanskHeltal(afrund(Kbeskaeftigelsesfradrag))

	// Opgørelse af jobfradrag
	// Grundlaget udgør det samme som for beskæftigelsesfradraget
	
	var Mjobfradragsgrundlag = Math.max(0,Mbeskaeftigelsesfradragsgrundlag - bundgraense_jobfradrag)
	var Mjobfradrag = Math.min(Mjobfradragsgrundlag * jobfradragsprocent,maksimalt_jobfradrag)

	form.Mjobfradrag = tilDanskHeltal(afrund(Mjobfradrag))

	var Kjobfradragsgrundlag = Math.max(0,Kbeskaeftigelsesfradragsgrundlag - bundgraense_jobfradrag)
	var Kjobfradrag = Math.min(Kjobfradragsgrundlag * jobfradragsprocent,maksimalt_jobfradrag)

	form.Kjobfradrag = tilDanskHeltal(afrund(Kjobfradrag))

	// Opgørelse af ekstra pensionsfradrag
	var MmereEnd15AarFolkepension = form.MmereEnd15AarFolkepension
	var KmereEnd15AarFolkepension = form.KmereEnd15AarFolkepension
	
	var MekstraPensionsfradraggrundlag = Math.min(maksimaltEkstraPensionsfradrag,parse(form.MrateArbejdsgiveradm)+parse(form.Mrate))

	if (MmereEnd15AarFolkepension) {
		var MekstraPensionsfradrag = ekstraPensionsfradragprocent1MereEnd5aar * MekstraPensionsfradraggrundlag;
	} else {
		var MekstraPensionsfradrag = ekstraPensionsfradragprocent15aarEllerMindre * MekstraPensionsfradraggrundlag;
	}

	form.MekstraPensionsfradrag = tilDanskHeltal(afrund(MekstraPensionsfradrag))

	var KekstraPensionsfradraggrundlag = Math.min(maksimaltEkstraPensionsfradrag,parse(form.KrateArbejdsgiveradm)+parse(form.Krate))

	if (KmereEnd15AarFolkepension) {
		var KekstraPensionsfradrag = ekstraPensionsfradragprocent1MereEnd5aar * KekstraPensionsfradraggrundlag;
	} else {
		var KekstraPensionsfradrag = ekstraPensionsfradragprocent15aarEllerMindre * KekstraPensionsfradraggrundlag;
	}

	form.KekstraPensionsfradrag = tilDanskHeltal(afrund(KekstraPensionsfradrag))
	
	// Opgørelse af ligningsmæssige fradrag
	
	MligningsmaessigeFradrag =
		parse(form.Mbefordring)
		+ parse(form.Mfagligt)
		+ parse(form.MoevrigeLoenmodtagerudgifter)
		+ parse(form.Maegtefaellebidrag)
		+ parse(form.MandreLignings)
		+ Mbeskaeftigelsesfradrag
		+ Mjobfradrag
		+ MekstraPensionsfradrag

	form.MligningsmaessigeFradrag = tilDanskHeltal(afrund(MligningsmaessigeFradrag))

	KligningsmaessigeFradrag =
		parse(form.Kbefordring)
		+ parse(form.Kfagligt)
		+ parse(form.KoevrigeLoenmodtagerudgifter)
		+ parse(form.Kaegtefaellebidrag)
		+ parse(form.KandreLignings)
		+ Kbeskaeftigelsesfradrag
		+ Kjobfradrag
		+ KekstraPensionsfradrag

	form.KligningsmaessigeFradrag = tilDanskHeltal(afrund(KligningsmaessigeFradrag))
	
	// skattepligtig indkomst
	MskattepligtigIndkomst =
		MpersonligIndkomst
		+ Mkapitalindkomst
		- MligningsmaessigeFradrag

	form.MskattepligtigIndkomst = tilDanskHeltal(afrund(MskattepligtigIndkomst))

	KskattepligtigIndkomst =
		KpersonligIndkomst
		+ Kkapitalindkomst
		- KligningsmaessigeFradrag

	form.KskattepligtigIndkomst = tilDanskHeltal(afrund(KskattepligtigIndkomst))

	// *************
	// Aktieindkomst
	// *************
	Maktieindkomst =
		parse(form.M61)
		+ parse(form.M64)

	form.Maktieindkomst = tilDanskHeltal(afrund(Maktieindkomst))

	Kaktieindkomst =
		parse(form.K61)
		+ parse(form.K64)

	form.Kaktieindkomst = tilDanskHeltal(afrund(Kaktieindkomst))
	
	return form
}

function skatteberegning(form:intputType) {
fatalFejl = false // Hvis sand: Resultatside vises ikke. Variablen er global

// her ved man, at alle oplysninger er (forsøgt) indtastet
// Der er allerede på et tidligere tidspunkt givet advarsel

if (skatteorakel) {
	// Disse fejlmeddelser vises ikke, hvis blot skatteberegning

}

// der tillades ikke negativ skattepligtig eller personlig indkomst
if (MpersonligIndkomst < 0 ||
	KpersonligIndkomst < 0) {
		console.error("Det forudsættes, at den personlige indkomst er positiv!")
		fatalFejl = true
} else {

	var gift = form.gift
	// Hvis der er angivet en indkomst under "ægtefælle", er man nok gift -> giv advarsel
	if (!gift && KskattepligtigIndkomst != 0) {
		console.error("Du har angivet en indkomst for din ægtefælle, men samtidigt oplyst, at du ikke er gift!")
		fatalFejl = true
	}

	if (!gift && Kaktieindkomst != 0) {
		console.error("Du har angivet en aktieindkomst for din ægtefælle, men samtidigt oplyst, at du ikke er gift!")
		fatalFejl = true
	}

/*
	// Hvis man har angivet, at man er gift, men ægtefællen ikke har nogen skattepligtig indkomst,
	// er der nok noget galt -> giv advarsel
	if (gift && KskattepligtigIndkomst == 0) {
		console.error("Muligvis mangler der oplysninger! Du har angivet, at du er gift, men din ægtefælles skattepligtige indkomst er 0!")
	}
*/

	var Munder18 = form.Munder18
	var Kunder18 = form.Kunder18
	var MmedlemFolkekirke = form.MmedlemFolkekirke
	var KmedlemFolkekirke = form.KmedlemFolkekirke

	// Fælles for kommunal skat og bundskat
	var Mpersonfradrag
	var Kpersonfradrag

	if (Munder18) {	
		Mpersonfradrag = personfradragUnge
	} else {
		Mpersonfradrag = personfradrag
	}

	if (Kunder18) {	
		Kpersonfradrag = personfradragUnge
	} else {
		Kpersonfradrag = personfradrag
	}

	////////////////////////////
	// Kommunal skat
	////////////////////////////
	// jfr. lovbek. nr. 770 af 13. oktober 1999

	var MkommSkatprc
	var KkommSkatprc

	var MkommSkat
	var KkommSkat
	var kommSkatIalt // samlet kommunal skat (for ægtefæller = sum)

	if (MmedlemFolkekirke) {
		MkommSkatprc = kommuneprc + sundhedsbidragprc + kirkeprc
	} else {
		MkommSkatprc = kommuneprc + sundhedsbidragprc
	}

	if (KmedlemFolkekirke) {
		KkommSkatprc = kommuneprc + sundhedsbidragprc + kirkeprc
	} else {
		KkommSkatprc = kommuneprc + sundhedsbidragprc
	}

	var MberegningsgrundlagKomm
	var KberegningsgrundlagKomm

	form.MpersonfradragKomm = tilDanskHeltal((-1) * afrund(Mpersonfradrag))

	if (gift) {
		form.KpersonfradragKomm = tilDanskHeltal((-1) * afrund(Kpersonfradrag))
	}

	form.MskattepligtigIndkomstKomm = tilDanskHeltal(afrund(MskattepligtigIndkomst))

	MberegningsgrundlagKomm = MskattepligtigIndkomst - Mpersonfradrag
	form.MberegningsgrundlagKomm = tilDanskHeltal(afrund(MberegningsgrundlagKomm))

	MkommSkat = MberegningsgrundlagKomm * (MkommSkatprc / 100)
	form.MkommSkat = tilDanskHeltal(afrund(MkommSkat))

	form.MkommSkatprc = afrund2dec(MkommSkatprc)
	if (gift) {
		form.KkommSkatprc = afrund2dec(KkommSkatprc)
	
		form.KskattepligtigIndkomstKomm = tilDanskHeltal(afrund(KskattepligtigIndkomst))

		KberegningsgrundlagKomm = KskattepligtigIndkomst - Kpersonfradrag
		form.KberegningsgrundlagKomm = tilDanskHeltal(afrund(KberegningsgrundlagKomm))

		KkommSkat = KberegningsgrundlagKomm * (KkommSkatprc / 100)
		form.KkommSkat = tilDanskHeltal(afrund(KkommSkat))

		// evt. negativ skat modregnes først i ægtefællens skat, jfr. PSL § 13, stk. 2 og PSL § 10, stk. 3
		kommSkatIalt = MkommSkat + KkommSkat
	} else {
		kommSkatIalt = MkommSkat
	}

	// evt. negativ skat modregnes i øvrige skatter, jfr. PSL §§ 9, stk. 1, og 13, stk. 1
	form.kommSkatIalt = tilDanskHeltal(afrund(kommSkatIalt))

	// kommunal skat [slut]

	///////////////////
	// Bundskat
	///////////////////
	// Der tages ikke højde for § 25a og § 27a i personskatteloven, jfr. lovbek. nr. 918 af 4/10-2000
	// Det betyder, at skatten vil kunne være lavere end beregnet her

	form.bundskatprc = bundskatprc

	var MberegningsgrundlagBund
	var KberegningsgrundlagBund

	var MpositivKapitalindkomstBund
	var KpositivKapitalindkomstBund

	var Mbundskat
	var Kbundskat
	var bundskatIalt // samlet bundskat

	form.MpersonligIndkomstBund = tilDanskHeltal(afrund(MpersonligIndkomst))
	form.MpersonfradragBund = tilDanskHeltal((-1) * afrund(Mpersonfradrag))

	if (gift) {
		form.KpersonligIndkomstBund = tilDanskHeltal(afrund(KpersonligIndkomst))

		if (Mkapitalindkomst >= 0) {
			if (Kkapitalindkomst >= 0) {
				// både skatteyder og ægtefælle har positiv kapitalindkomst
				MpositivKapitalindkomstBund = Mkapitalindkomst
				KpositivKapitalindkomstBund = Kkapitalindkomst
			} else {
				// ægtefælle har negativ kapitalindkomst -> modregning, jfr. PSL § 6, stk. 4
				MpositivKapitalindkomstBund = pos(Mkapitalindkomst + Kkapitalindkomst)
				KpositivKapitalindkomstBund = 0
			}
		} else {
			// skatteyders kapitalindkomst er negativ
			if (Kkapitalindkomst >= 0) {
				// ægtefælles kapitalindkomst positiv -> modregning, jfr. PSL § 6, stk. 4

				MpositivKapitalindkomstBund = 0
				KpositivKapitalindkomstBund = pos(Mkapitalindkomst + Kkapitalindkomst)
							
			} else {
				// ægtefælle har også negativ kapitalindkomst 
				MpositivKapitalindkomstBund = 0
				KpositivKapitalindkomstBund = 0
			}
		}

		form.MpositivKapitalindkomstBund = tilDanskHeltal(afrund(MpositivKapitalindkomstBund))
		form.KpositivKapitalindkomstBund = tilDanskHeltal(afrund(KpositivKapitalindkomstBund))

		form.KpersonfradragBund = tilDanskHeltal((-1) * afrund(Kpersonfradrag))

		MberegningsgrundlagBund =
			MpersonligIndkomst
			+ MpositivKapitalindkomstBund
			- Mpersonfradrag

		KberegningsgrundlagBund =
			KpersonligIndkomst
			+ KpositivKapitalindkomstBund
			- Kpersonfradrag

		form.MberegningsgrundlagBund = tilDanskHeltal(afrund(MberegningsgrundlagBund))
		form.KberegningsgrundlagBund = tilDanskHeltal(afrund(KberegningsgrundlagBund))

		Mbundskat = MberegningsgrundlagBund * (bundskatprc / 100)
		form.Mbundskat = tilDanskHeltal(afrund(Mbundskat))

		Kbundskat = KberegningsgrundlagBund * (bundskatprc / 100)
		form.Kbundskat = tilDanskHeltal(afrund(Kbundskat))

		bundskatIalt = Mbundskat + Kbundskat
	} else { // ugift
		MpositivKapitalindkomstBund = pos(Mkapitalindkomst)

		form.MpositivKapitalindkomstBund = tilDanskHeltal(afrund(MpositivKapitalindkomstBund))

		MberegningsgrundlagBund =
			MpersonligIndkomst
			+ MpositivKapitalindkomstBund
			- Mpersonfradrag

		form.MberegningsgrundlagBund = tilDanskHeltal(afrund(MberegningsgrundlagBund))

		Mbundskat = MberegningsgrundlagBund * (bundskatprc / 100)
		form.Mbundskat = tilDanskHeltal(afrund(Mbundskat))

		bundskatIalt = Mbundskat
	}

	// evt. negativ skat modregnes i øvrige skatter, jfr. PSL §§ 9, stk. 1, og 13, stk. 1
	form.bundskatIalt = tilDanskHeltal(afrund(bundskatIalt))

	// bundskat [slut]

	////////////////
	// Topskat
	////////////////
	
	// Der beregnes topskat af
	// a. Personlig indkomst + indskud på kapitalpension
	// b. Positiv nettokapitalindkomst

	// Topskatteprocent for personlig indkomst + indskud på kapitalpension reduceres, hvis det skrå skatteloft er passeret, jfr. PSL § 19
	var samletprc = kommuneprc + sundhedsbidragprc + bundskatprc + topskatprc
	var topskatprcReduceret

	if (samletprc > skatteloftprc) {
		topskatprcReduceret = topskatprc - forskelToDecimaler(samletprc,skatteloftprc) // Fra 2008 med 2 decimaler
	} else {
		topskatprcReduceret = topskatprc
	}

	form.topskatprc_personlig_indkomst = topskatprcReduceret

	// Topskatteprocent for positiv nettokapitalindkomst reduceres, hvis det skrå skatteloft for positiv nettokapitalindkomst er passeret
	var samletprc = kommuneprc + sundhedsbidragprc + bundskatprc + topskatprc
	var topskatprcReduceret_positivkapitalindkomst

	if (samletprc > skatteloftprc_positivkapitalindkomst) {
		topskatprcReduceret_positivkapitalindkomst = topskatprc - forskelToDecimaler(samletprc,skatteloftprc_positivkapitalindkomst)
	} else {
		topskatprcReduceret_positivkapitalindkomst = topskatprc
	}

	form.topskatprc_positivkapitalindkomst = afrund2dec(topskatprcReduceret_positivkapitalindkomst)

	var MpositivKapitalindkomstTop
	var KpositivKapitalindkomstTop
	
	var samlPositivKapitalindkomst

	var MberegningsgrundlagTop_personlig_indkomst
	var KberegningsgrundlagTop_personlig_indkomst

	var MberegningsgrundlagTop_nettokapitalindkomst
	var KberegningsgrundlagTop_nettokapitalindkomst

	// Er gjort til global variabel: var Mtopskat
	var Ktopskat
	var topskatIalt // samlet topskat (for ægtefæller = sum); kan ikke modregnes som bundskat 

	form.MpersonligIndkomstTop = tilDanskHeltal(afrund(MpersonligIndkomst))
	form.MindskudKapitalpension = tilDanskHeltal(afrund(MindskudKapitalpension))
	form.MarbejdsgiverIndskudKapitalpension1 = tilDanskHeltal(afrund(MarbejdsgiverIndskudKapitalpension))
	form.topskatgraense1 = tilDanskHeltal((-1) * afrund(topskatgraense))

	var MpersonligIndkomstogIndskudPension = MpersonligIndkomst
		+ MindskudKapitalpension
		+ MarbejdsgiverIndskudKapitalpension;

	if (gift) {
		form.KpersonligIndkomstTop = tilDanskHeltal(afrund(KpersonligIndkomst))
		form.KindskudKapitalpension = tilDanskHeltal(afrund(KindskudKapitalpension))
		form.KarbejdsgiverIndskudKapitalpension1 = tilDanskHeltal(afrund(KarbejdsgiverIndskudKapitalpension))

		var KpersonligIndkomstogIndskudPension = KpersonligIndkomst
			+ KindskudKapitalpension
			+ KarbejdsgiverIndskudKapitalpension;

		if (Mkapitalindkomst >= 0) {
			if (Kkapitalindkomst >= 0) {
				// både skatteyder og ægtefælle har positiv kapitalindkomst
				MpositivKapitalindkomstTop = Mkapitalindkomst
				KpositivKapitalindkomstTop = Kkapitalindkomst
			} else {
				// ægtefælle har negativ kapitalindkomst -> modregning, jfr. PSL § 6 a, stk. 3
				MpositivKapitalindkomstTop = pos(Mkapitalindkomst + Kkapitalindkomst)
				KpositivKapitalindkomstTop = 0
			}
		} else {
			// skatteyders kapitalindkomst er negativ
			if (Kkapitalindkomst >= 0) {
				// ægtefælles kapitalindkomst positiv -> modregning, jfr. PSL § 6 a, stk. 3
				MpositivKapitalindkomstTop = 0
				KpositivKapitalindkomstTop = pos(Mkapitalindkomst + Kkapitalindkomst)
			} else {
				// ægtefælle har også negativ kapitalindkomst 
				MpositivKapitalindkomstTop = 0
				KpositivKapitalindkomstTop = 0
			}
		}

		samlPositivKapitalindkomst = MpositivKapitalindkomstTop + KpositivKapitalindkomstTop

		// Bundfradrag for positiv nettokapitalindkomst
		var bundfradrag_positiv_nettokapitalindkomst = 2 * bundfradrag_positiv_nettokapitalindkomst_konstant;

		if (samlPositivKapitalindkomst < bundfradrag_positiv_nettokapitalindkomst) {
			samlPositivKapitalindkomst=0;
		} else {
			samlPositivKapitalindkomst -= bundfradrag_positiv_nettokapitalindkomst;
		}

		if (MpersonligIndkomstogIndskudPension >= KpersonligIndkomstogIndskudPension) { // 10/11-2010
			// beregning på toppen af skatteyderens indkomst
			MpositivKapitalindkomstTop = samlPositivKapitalindkomst
			KpositivKapitalindkomstTop = 0

			form.MpositivKapitalindkomstTop = tilDanskHeltal(afrund(MpositivKapitalindkomstTop))
			form.KpositivKapitalindkomstTop = tilDanskHeltal(afrund(KpositivKapitalindkomstTop))

			if (MpersonligIndkomstogIndskudPension >= topskatgraense) {
				var topskatgraense_positivkapitalindkomst = 0;
			} else {
				var topskatgraense_positivkapitalindkomst = topskatgraense - MpersonligIndkomstogIndskudPension;
			}

			form.topskatgraense3 = tilDanskHeltal((-1) * afrund(topskatgraense_positivkapitalindkomst));
			form.topskatgraense4 = 0;

			// B. Beregning af topskat af positiv nettokapitalindkomst
			var MberegningsgrundlagTop_positivkapitalindkomst = MpositivKapitalindkomstTop - topskatgraense_positivkapitalindkomst;

			form.MberegningsgrundlagTop_positivkapitalindkomst = tilDanskHeltal(afrund(MberegningsgrundlagTop_positivkapitalindkomst))
			form.KberegningsgrundlagTop_positivkapitalindkomst = 0;

			var Mtopskat_positivkapitalindkomst = MberegningsgrundlagTop_positivkapitalindkomst * (topskatprcReduceret_positivkapitalindkomst / 100)
			var Ktopskat_positivkapitalindkomst = 0;

			form.Mtopskat_positivkapitalindkomst = tilDanskHeltal(afrund(Mtopskat_positivkapitalindkomst))

			form.Ktopskat_positivkapitalindkomst = 0;
		} else {
			// beregning på toppen af ægtefællens indkomst
			KpositivKapitalindkomstTop = samlPositivKapitalindkomst
			MpositivKapitalindkomstTop = 0

			form.MpositivKapitalindkomstTop = 0
			form.KpositivKapitalindkomstTop = tilDanskHeltal(afrund(KpositivKapitalindkomstTop))

			if (KpersonligIndkomstogIndskudPension >= topskatgraense) {
				topskatgraense_positivkapitalindkomst = 0;
			} else {
				topskatgraense_positivkapitalindkomst = topskatgraense - KpersonligIndkomstogIndskudPension;
			}

			form.topskatgraense3 = 0
			form.topskatgraense4 = tilDanskHeltal((-1) * afrund(topskatgraense_positivkapitalindkomst));

			// B. Beregning af topskat af positiv nettokapitalindkomst
			var KberegningsgrundlagTop_positivkapitalindkomst = KpositivKapitalindkomstTop - topskatgraense_positivkapitalindkomst;

			form.MberegningsgrundlagTop_positivkapitalindkomst = 0;
			form.KberegningsgrundlagTop_positivkapitalindkomst = tilDanskHeltal(afrund(KberegningsgrundlagTop_positivkapitalindkomst))

			form.Mtopskat_positivkapitalindkomst = 0;

			Mtopskat_positivkapitalindkomst = 0;
			Ktopskat_positivkapitalindkomst = KberegningsgrundlagTop_positivkapitalindkomst * (topskatprcReduceret_positivkapitalindkomst / 100)

			form.Ktopskat_positivkapitalindkomst = tilDanskHeltal(afrund(Ktopskat_positivkapitalindkomst))
		}

		form.topskatgraense1 = tilDanskHeltal((-1) * afrund(topskatgraense))
		form.topskatgraense2 = tilDanskHeltal((-1) * afrund(topskatgraense))

		// A. Beregning af topskat af personlig indkomst og indskud på kapitalpension

		MberegningsgrundlagTop_personlig_indkomst = MpersonligIndkomstogIndskudPension
			- topskatgraense

		KberegningsgrundlagTop_personlig_indkomst = KpersonligIndkomstogIndskudPension
			- topskatgraense

		form.MberegningsgrundlagTop_personlig_indkomst = tilDanskHeltal(afrund(MberegningsgrundlagTop_personlig_indkomst))
		form.KberegningsgrundlagTop_personlig_indkomst = tilDanskHeltal(afrund(KberegningsgrundlagTop_personlig_indkomst))

		var Mtopskat_personlig_indkomst = MberegningsgrundlagTop_personlig_indkomst * (topskatprcReduceret / 100)
		form.Mtopskat_personlig_indkomst = tilDanskHeltal(afrund(Mtopskat_personlig_indkomst))

		var Ktopskat_personlig_indkomst = KberegningsgrundlagTop_personlig_indkomst * (topskatprcReduceret / 100)
		form.Ktopskat_personlig_indkomst = tilDanskHeltal(afrund(Ktopskat_personlig_indkomst))


		// der kan ikke overføres uudnyttet bundfradrag som ved mellemskat		
		var topskatIalt_personlig_indkomst = pos(Mtopskat_personlig_indkomst) + pos(Ktopskat_personlig_indkomst)
		var topskatIalt_positivkapitalindkomst = pos(Mtopskat_positivkapitalindkomst) + pos(Ktopskat_positivkapitalindkomst)

		topskatIalt = topskatIalt_personlig_indkomst + topskatIalt_positivkapitalindkomst

	} else { // ugift
		MpositivKapitalindkomstTop = pos(Mkapitalindkomst)

		// Bundfradrag for positiv nettokapitalindkomst
		bundfradrag_positiv_nettokapitalindkomst = bundfradrag_positiv_nettokapitalindkomst_konstant;

		if (MpositivKapitalindkomstTop < bundfradrag_positiv_nettokapitalindkomst) {
			MpositivKapitalindkomstTop=0;
		} else {
			MpositivKapitalindkomstTop -= bundfradrag_positiv_nettokapitalindkomst;
		}

		form.MpositivKapitalindkomstTop = tilDanskHeltal(afrund(MpositivKapitalindkomstTop))

		// A. Beregning af topskat af personlig indkomst og indskud på kapitalpension

		MberegningsgrundlagTop_personlig_indkomst = MpersonligIndkomstogIndskudPension
			- topskatgraense

		form.MberegningsgrundlagTop_personlig_indkomst = tilDanskHeltal(afrund(MberegningsgrundlagTop_personlig_indkomst))
		form.KberegningsgrundlagTop_personlig_indkomst = "ugift"

		Mtopskat_personlig_indkomst = MberegningsgrundlagTop_personlig_indkomst * (topskatprcReduceret / 100)
		form.Mtopskat_personlig_indkomst = tilDanskHeltal(afrund(Mtopskat_personlig_indkomst))
		form.Ktopskat_personlig_indkomst = "ugift"

		// B. Beregning af topskat af positiv nettokapitalindkomst

		if (MpersonligIndkomstogIndskudPension >= topskatgraense) {
			topskatgraense_positivkapitalindkomst = 0;
		} else {
			topskatgraense_positivkapitalindkomst = topskatgraense - MpersonligIndkomstogIndskudPension;
		}

		form.topskatgraense3 = tilDanskHeltal((-1) * afrund(topskatgraense_positivkapitalindkomst));
		form.topskatgraense4 = "ugift"

		MberegningsgrundlagTop_positivkapitalindkomst = MpositivKapitalindkomstTop
			- topskatgraense_positivkapitalindkomst;

		form.MberegningsgrundlagTop_positivkapitalindkomst = tilDanskHeltal(afrund(MberegningsgrundlagTop_positivkapitalindkomst))
		form.KberegningsgrundlagTop_positivkapitalindkomst = "ugift";

		Mtopskat_positivkapitalindkomst = MberegningsgrundlagTop_positivkapitalindkomst * (topskatprcReduceret_positivkapitalindkomst / 100)
		Ktopskat_positivkapitalindkomst = 0;

		form.Mtopskat_positivkapitalindkomst = tilDanskHeltal(afrund(Mtopskat_positivkapitalindkomst))

		topskatIalt_personlig_indkomst = pos(Mtopskat_personlig_indkomst);
		topskatIalt_positivkapitalindkomst = pos(Mtopskat_positivkapitalindkomst);

		topskatIalt = topskatIalt_personlig_indkomst + topskatIalt_positivkapitalindkomst
	}


	form.bundfradrag_positiv_nettokapitalindkomst = tilDanskHeltal(bundfradrag_positiv_nettokapitalindkomst);
	form.topskatIalt_personlig_indkomst = tilDanskHeltal(afrund(topskatIalt_personlig_indkomst))
	form.topskatIalt_positivkapitalindkomst = tilDanskHeltal(afrund(topskatIalt_positivkapitalindkomst))

	// skat kan kun blive positiv (i.e. kan ikke modregnes)

	form.topskatIalt = tilDanskHeltal(afrund(topskatIalt))

	// topskat [slut]

	///////////////////////////////////
	// Ejendomsværdiskat
	///////////////////////////////////
	var ejendomsvaerdiskatIalt	

	// Helårsbolig
	var ejendomsvaerdi 
	var ejendomsvaerdiskatUnder 
	var ejendomsvaerdiskatOver 
	var ejendomsvaerdiskatHelaarsbolig

	var nedslagsprc
	var nedslag

	//////////////////////
	// Aktieskat
	//////////////////////

	var samletAktieindkomst
	var samletProgressionsgraense
	var aktieindkomstUnderGraense
	var aktieindkomstOverGraense

	var aktieskatUnderGraense
	var aktieskatOverGraense

	var aktieskatIalt
	
	form.Maktieindkomst1 = tilDanskHeltal(afrund(Maktieindkomst))
	samletAktieindkomst = Maktieindkomst

	form.Maktiegraense = tilDanskHeltal(afrund(aktieskatgrundbeloeb))
	samletProgressionsgraense = aktieskatgrundbeloeb

	if (gift) {
		form.Kaktieindkomst1 = tilDanskHeltal(afrund(Kaktieindkomst))
		samletAktieindkomst += Kaktieindkomst

		form.Kaktiegraense = tilDanskHeltal(afrund(aktieskatgrundbeloeb))
		samletProgressionsgraense += aktieskatgrundbeloeb

	}

	form.samletAktieindkomst = tilDanskHeltal(afrund(samletAktieindkomst))
	form.samletProgressionsgraense = tilDanskHeltal(afrund(samletProgressionsgraense))

	if (samletAktieindkomst <= samletProgressionsgraense) {
		if (samletAktieindkomst >= 0) {
			aktieindkomstUnderGraense = samletAktieindkomst 
			aktieindkomstOverGraense = 0
		} else {
			// samlet aktieindkomst er negativ
			if (samletAktieindkomst * (-1) <= samletProgressionsgraense) {
				aktieindkomstUnderGraense = samletAktieindkomst
				aktieindkomstOverGraense = 0
			} else {
				aktieindkomstUnderGraense = (-1) * samletProgressionsgraense
				aktieindkomstOverGraense = samletAktieindkomst - aktieindkomstUnderGraense
			}
		}
	} else {
		// samlet aktieindkomst er over progressionsgrænsen
		aktieindkomstUnderGraense = samletProgressionsgraense
		aktieindkomstOverGraense = samletAktieindkomst - aktieindkomstUnderGraense
	}

	form.aktieindkomstUnderGraense = tilDanskHeltal(afrund(aktieindkomstUnderGraense))
	form.aktieindkomstOverGraense = tilDanskHeltal(afrund(aktieindkomstOverGraense))

	aktieskatUnderGraense = aktieindkomstUnderGraense * (underAktieskatprc / 100) 
	aktieskatOverGraense = aktieindkomstOverGraense * (overAktieskatprc / 100) 

	form.aktieskatUnderGraense = tilDanskHeltal(afrund(aktieskatUnderGraense))
	form.aktieskatOverGraense = tilDanskHeltal(afrund(aktieskatOverGraense))

	aktieskatIalt = aktieskatUnderGraense + aktieskatOverGraense
	
	form.aktieskatIalt = tilDanskHeltal(afrund(aktieskatIalt))

	form.aktieskatprcUnderGraense = underAktieskatprc
	form.aktieskatprcOverGraense = overAktieskatprc

	// aktieskat [slut]

	//////////////////////////////////
	// AMB og ATP-bidrag
	//////////////////////////////////

	// beregningen er foretaget oven for i indkomstopgørelse
	form.AMBATPprc = AMBprc

	var MberegningsgrundlagAMB
	var KberegningsgrundlagAMB
	var AMBIalt

	form.MloenFoerAMB_Result = tilDanskHeltal(afrund(MloenFoerAMB))

	MberegningsgrundlagAMB = MloenFoerAMB
	form.MberegningsgrundlagAMB = tilDanskHeltal(afrund(MberegningsgrundlagAMB))

	form.MAMB = tilDanskHeltal(afrund(MAMB))

	if (gift) {
		form.KloenFoerAMB = tilDanskHeltal(afrund(KloenFoerAMB))

		KberegningsgrundlagAMB = KloenFoerAMB
		form.KberegningsgrundlagAMB = tilDanskHeltal(afrund(KberegningsgrundlagAMB))
		
		form.KAMB = tilDanskHeltal(afrund(KAMB))

		AMBIalt = MAMB + KAMB
	} else {

		AMBIalt = MAMB
	}

	form.AMBIalt = tilDanskHeltal(afrund(AMBIalt))
	// AMB og ATP-bidrag [slut]

// ** Start: Ny 2012 ****

	///////////////////////////////////////
	// Nedslag negativ nettokapitalindkomst
	///////////////////////////////////////

	// Jf. personskattelovens § 11

	var nedslagsgraenseNegativKapitalindkomst;

	form.nedslagNegativNettokapitalindkomstprc = nedslagNegativNettokapitalindkomstprc

	form.Mkapitalindkomst_nedslag = tilDanskHeltal(afrund(Mkapitalindkomst));
	if (gift) {
		nedslagsgraenseNegativKapitalindkomst = 2 * 50000;
		form.Kkapitalindkomst_nedslag = tilDanskHeltal(afrund(Kkapitalindkomst));
	} else {
		nedslagsgraenseNegativKapitalindkomst = 50000;
	}

	if (Mkapitalindkomst + Kkapitalindkomst < 0) {
		var SamletNegativKapitalindkomst_nedslag = (-1)*(Mkapitalindkomst + Kkapitalindkomst);

		if (SamletNegativKapitalindkomst_nedslag > nedslagsgraenseNegativKapitalindkomst) {
			SamletNegativKapitalindkomst_nedslag = nedslagsgraenseNegativKapitalindkomst;
		}
	} else {
		SamletNegativKapitalindkomst_nedslag = 0;
	}

	form.SamletNegativKapitalindkomst_nedslag = tilDanskHeltal(afrund((-1)*SamletNegativKapitalindkomst_nedslag));

	var NedslagNegativKapitalindkomst;

	NedslagNegativKapitalindkomst = SamletNegativKapitalindkomst_nedslag * (nedslagNegativNettokapitalindkomstprc/100);
	
	form.NedslagNegativKapitalindkomst =  tilDanskHeltal(afrund((-1)*NedslagNegativKapitalindkomst));

	form.IaltNedslagNegativKapitalindkomst = tilDanskHeltal(afrund((-1)*NedslagNegativKapitalindkomst));

	// Nedslag negativ nettokapitalindkomst [slut]

// ** Slut: Ny 2012 ****

	// Samlet skat inkl. AMB og ATP-bidrag
	skatIalt = pos(kommSkatIalt
				+ bundskatIalt
				+ topskatIalt
				+ aktieskatOverGraense
				- NedslagNegativKapitalindkomst)

		// skat efter § 8 a, stk. 1, er endelig - ikke modregning af ovenstående i skatten
	skatIalt += aktieskatUnderGraense

		// der kan ikke modregnes i ejendomsværdiskat og arbejdsmarkedsbidrag
	skatIalt = pos(skatIalt) + AMBIalt

	form.skatIalt = tilDanskHeltal(afrund(skatIalt))


	var skatFastEjendomIalt = ejendomsvaerdiskatIalt;
	form.skatFastEjendomIalt = tilDanskHeltal(afrund(skatFastEjendomIalt))

	return form

}
}

// Hjælpefunktioner
function forskelEenDecimal(x:number, y:number) {
	// returnerer x-y med en decimal
	return (Math.round(x*10 - y*10) / 10)
}

function forskelToDecimaler(x:number, y:number) {
	// returnerer x-y med to decimal
	return (Math.round(x*100 - y*100) / 100)
}

function kommune (skatteprocenter, hus) {
	var i
	var j

	kommunenavn = "intet"

	// skatteprocenter har format: "19.9 0.57 25.74"
	// kommune, kirke, grundskyldpromille

	i = findCiffer(skatteprocenter,0)
	// i peger nu på første ciffer

	j = findIkkeCiffer(skatteprocenter,i)
	// j peger nu på første ikke-ciffer
	if (hus=="helaarsbolig") {
		kommuneprc = parseFloat(skatteprocenter.substring(i,j))
	}

	i = findCiffer(skatteprocenter,j)
	// i peger nu på første ciffer

	j = findIkkeCiffer(skatteprocenter,i)
	// j peger nu på første ikke-ciffer
	if (hus=="helaarsbolig") {
		kirkeprc = parseFloat(skatteprocenter.substring(i,j))
	}

	i = findCiffer(skatteprocenter,j)
	// i peger nu på første ciffer

	j = findIkkeCiffer(skatteprocenter,i)
	// j peger nu på første ikke-ciffer

	if (hus=="helaarsbolig") {
		grundskyldpromille = parseFloat(skatteprocenter.substring(i,j));
	} else {
		grundskyldpromilleSommerhus = parseFloat(skatteprocenter.substring(i,j));
	}
}

function findCiffer (str,start) {
	// Finder den første position, hvor der står et ciffer
	// regnet fra start (= indexOf("ciffer",start))
	// MSIE 3 implementerer ikke indexOf

	var i

	i = start
	while (	(str.charAt(i) != '0') &&
		(str.charAt(i) != '1') && 
		(str.charAt(i) != '2') && 
		(str.charAt(i) != '3') &&
		(str.charAt(i) != '4') && 
		(str.charAt(i) != '5') && 
		(str.charAt(i) != '6') && 
		(str.charAt(i) != '7') && 
		(str.charAt(i) != '8') && 
		(str.charAt(i) != '9'))
	{i +=1}

	return i		
}

function findIkkeCiffer (str,start) {
	// Finder den første position, hvor der ikke står et ciffer eller et decimalpunktum (.)
	// regnet fra start (= indexOf("x",start))
	// MSIE 3 implementerer ikke indexOf

	var i

	i = start
	while ( (str.charAt(i) == '.') ||
		(str.charAt(i) == '0') || 
		(str.charAt(i) == '1') || 
		(str.charAt(i) == '2') || 
		(str.charAt(i) == '3') || 
		(str.charAt(i) == '4') || 
		(str.charAt(i) == '5') || 
		(str.charAt(i) == '6') || 
		(str.charAt(i) == '7') || 
		(str.charAt(i) == '8') || 
		(str.charAt(i) == '9'))
	{i +=1}

	return i		
}

function pos(tal) {
	if (tal > 0) {
		return tal
	} else {
		return 0
	}
}

function afrund(tal) {
	return Math.round(tal)
}

function afrund2dec(tal) {
	return Math.round(tal*100) / 100
}

function parse(input:any) {
	if (!input) return 0
	return input;
}

function parse3(str:string):number {
	// Læser kun heltal
	let resultat = parseInt(str)

	if (isNaN(resultat)) {
		return 0
	} else {
		return resultat
	}
}

function tilDanskHeltal (heltal:number):number {
	// Funktionen returnerer en streng som repræsenterer tallet heltal med eventuelle punktummer som 1000-tals-adskillelse
	// Eksempel:
	// tilDanskHeltal(1000000) = "1.000.000"
	// tilDanskHeltal(-1000) = "-1.000"
	// Undersøg om tallet er negativt
	return heltal
}

let zzz = skatteberegning({MloenFoerAMB1: 100000});
console.log(zzz.skatIalt)