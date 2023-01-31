form = """var skatteorakel = false;
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
} else {
	alert ("Indkomstår ikke implementeret!")
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

function indkomstopgoerelse(form) {
	// omregning af personlig indkomst før AMB til efter AMB
	let MloenFoerAMB = parse(form.MloenFoerAMB1.value)
	let KloenFoerAMB = parse(form.KloenFoerAMB1.value)

	let MAMB = MloenFoerAMB * AMBprc / 100
	let KAMB = KloenFoerAMB * AMBprc / 100

	form.MAMB1.value = tilDanskHeltal(afrund(MAMB))
	form.KAMB1.value = tilDanskHeltal(afrund(KAMB))

	let Mloen = MloenFoerAMB - MAMB
	let Kloen = KloenFoerAMB - KAMB

	// Start: regn ud, om skatteyders indskud på kapitalpension overstiger maksimumgrænse
	// Er det tilfældet nedsættes indskudet på privattegnet kapitalpension
	// - og medregnes ikke ved beregning af topskat - da heller ikke bortseelsesret for arbejdsgiveradministreret ordning
	MindskudKapitalpension = parse(form.Mkapital.value)

	MarbejdsgiverIndskudKapitalpension = parse(form.MarbejdsgiverIndskudKapitalpension.value)

	let overskridelse = (MindskudKapitalpension + MarbejdsgiverIndskudKapitalpension)
			- maksimumKapitalpensionsfradrag
	if (overskridelse > 0) {
		alert("Der kan maksimalt fradrages " + tilDanskHeltal(maksimumKapitalpensionsfradrag) + " kr. ved indbetaling på kapitalpensioner!")

		if (MindskudKapitalpension > overskridelse) {
			var MfradragsberettigetIndskudKapitalpension = MindskudKapitalpension - overskridelse
		} else {
			var MfradragsberettigetIndskudKapitalpension = 0
		}

		form.Mkapital.value = MfradragsberettigetIndskudKapitalpension
	} else {
		MfradragsberettigetIndskudKapitalpension = MindskudKapitalpension
	}

	// Det overskydende beløb medregnes ikke ved beregning af topskat, jfr. personskatteloven § 7, stk. 1
	MindskudKapitalpension = MfradragsberettigetIndskudKapitalpension
	// Slut: regn ud, om indskud på kapitalpension overstiger maksimumgrænse

	// personlig indkomst
	MpersonligIndkomst =
		Mloen 
		+ parse(form.MandenPersonlig.value)
		- MfradragsberettigetIndskudKapitalpension
		- parse(form.Mrate.value)

	form.MpersonligIndkomst.value = tilDanskHeltal(afrund(MpersonligIndkomst))

	// Start: regn ud, om ægtefælles indskud på kapitalpension overstiger maksimumgrænse
	// Er det tilfældet nedsættes indskudet på privattegnet kapitalpension
	// - og medregnes ikke ved beregning af topskat - da heller ikke bortseelsesret for arbejdsgiveradministreret ordning
	KindskudKapitalpension = parse(form.Kkapital.value)
	KarbejdsgiverIndskudKapitalpension = parse(form.KarbejdsgiverIndskudKapitalpension.value)										

	overskridelse = (KindskudKapitalpension + KarbejdsgiverIndskudKapitalpension)
			- maksimumKapitalpensionsfradrag
	if (overskridelse > 0) {
		alert("Der kan maksimalt fradrages " + tilDanskHeltal(maksimumKapitalpensionsfradrag) + " kr. ved indbetaling på kapitalpensioner!")

		if (KindskudKapitalpension > overskridelse) {
			var KfradragsberettigetIndskudKapitalpension = KindskudKapitalpension - overskridelse
		} else {
			var KfradragsberettigetIndskudKapitalpension = 0
		}

		form.Kkapital.value = KfradragsberettigetIndskudKapitalpension
	} else {
		KfradragsberettigetIndskudKapitalpension = KindskudKapitalpension
	}

	// Det overskydende beløb medregnes ikke ved beregning af topskat, jfr. personskatteloven § 7, stk. 1
	KindskudKapitalpension = KfradragsberettigetIndskudKapitalpension
	// Slut: regn ud, om indskud på kapitalpension overstiger maksimumgrænse

	KpersonligIndkomst =
		Kloen 
		+ parse(form.KandenPersonlig.value)
		- KfradragsberettigetIndskudKapitalpension
		- parse(form.Krate.value)

	form.KpersonligIndkomst.value = tilDanskHeltal(afrund(KpersonligIndkomst))

	// kapitalindkomst
	Mkapitalindkomst =
		parse(form.Mrenteind.value)
		+ parse(form.MandenKapital.value)
		- parse(form.Mrenteud.value)

	form.Mkapitalindkomst.value = tilDanskHeltal(afrund(Mkapitalindkomst))

	Kkapitalindkomst =
		parse(form.Krenteind.value)
		+ parse(form.KandenKapital.value)
		- parse(form.Krenteud.value)

	form.Kkapitalindkomst.value = tilDanskHeltal(afrund(Kkapitalindkomst))

	// ligningsmæssige fradrag

	// Opgørelse af beskæftigelsesfradrag (fra indkomståret 2004)
	// Jfr. lov nr. 442 af 10. juni 2003

	// Ændret 17/12-2020 fra : Mbeskaeftigelsesfradragsgrundlag = Math.max(0,parse(form.MloenFoerAMB1.value)-parse(form.Mkapital.value)-parse(form.Mrate.value))

	var Mbeskaeftigelsesfradragsgrundlag = Math.max(0,parse(form.MloenFoerAMB1.value)+parse(form.MrateArbejdsgiveradm.value)) // 2/5-2021
	var Mbeskaeftigelsesfradrag = Math.min(Mbeskaeftigelsesfradragsgrundlag * beskaeftigelsesfradragsprocent,maksimumBeskaeftigelsesfradrag)

	form.Mbeskaeftigelsesfradrag.value = tilDanskHeltal(afrund(Mbeskaeftigelsesfradrag))

	// Ændret 17/12-2020 fra : Kbeskaeftigelsesfradragsgrundlag = Math.max(0,parse(form.KloenFoerAMB1.value)-parse(form.Kkapital.value)-parse(form.Krate.value))

	var Kbeskaeftigelsesfradragsgrundlag = Math.max(0,parse(form.KloenFoerAMB1.value)+parse(form.KrateArbejdsgiveradm.value)) // 2/5-2021
	var Kbeskaeftigelsesfradrag = Math.min(Kbeskaeftigelsesfradragsgrundlag * beskaeftigelsesfradragsprocent,maksimumBeskaeftigelsesfradrag)

	form.Kbeskaeftigelsesfradrag.value = tilDanskHeltal(afrund(Kbeskaeftigelsesfradrag))

	// Opgørelse af jobfradrag
	// Grundlaget udgør det samme som for beskæftigelsesfradraget
	
	var Mjobfradragsgrundlag = Math.max(0,Mbeskaeftigelsesfradragsgrundlag - bundgraense_jobfradrag)
	var Mjobfradrag = Math.min(Mjobfradragsgrundlag * jobfradragsprocent,maksimalt_jobfradrag)

	form.Mjobfradrag.value = tilDanskHeltal(afrund(Mjobfradrag))

	var Kjobfradragsgrundlag = Math.max(0,Kbeskaeftigelsesfradragsgrundlag - bundgraense_jobfradrag)
	var Kjobfradrag = Math.min(Kjobfradragsgrundlag * jobfradragsprocent,maksimalt_jobfradrag)

	form.Kjobfradrag.value = tilDanskHeltal(afrund(Kjobfradrag))

	// Opgørelse af ekstra pensionsfradrag
	var MmereEnd15AarFolkepension = form.MmereEnd15AarFolkepension[0].checked
	var KmereEnd15AarFolkepension = form.KmereEnd15AarFolkepension[0].checked
	
	var MekstraPensionsfradraggrundlag = Math.min(maksimaltEkstraPensionsfradrag,parse(form.MrateArbejdsgiveradm.value)+parse(form.Mrate.value))

	if (MmereEnd15AarFolkepension) {
		var MekstraPensionsfradrag = ekstraPensionsfradragprocent1MereEnd5aar * MekstraPensionsfradraggrundlag;
	} else {
		var MekstraPensionsfradrag = ekstraPensionsfradragprocent15aarEllerMindre * MekstraPensionsfradraggrundlag;
	}

	form.MekstraPensionsfradrag.value = tilDanskHeltal(afrund(MekstraPensionsfradrag))

	var KekstraPensionsfradraggrundlag = Math.min(maksimaltEkstraPensionsfradrag,parse(form.KrateArbejdsgiveradm.value)+parse(form.Krate.value))

	if (KmereEnd15AarFolkepension) {
		var KekstraPensionsfradrag = ekstraPensionsfradragprocent1MereEnd5aar * KekstraPensionsfradraggrundlag;
	} else {
		var KekstraPensionsfradrag = ekstraPensionsfradragprocent15aarEllerMindre * KekstraPensionsfradraggrundlag;
	}

	form.KekstraPensionsfradrag.value = tilDanskHeltal(afrund(KekstraPensionsfradrag))
	
	// Opgørelse af ligningsmæssige fradrag
	
	MligningsmaessigeFradrag =
		parse(form.Mbefordring.value)
		+ parse(form.Mfagligt.value)
		+ parse(form.MoevrigeLoenmodtagerudgifter.value)
		+ parse(form.Maegtefaellebidrag.value)
		+ parse(form.MandreLignings.value)
		+ Mbeskaeftigelsesfradrag
		+ Mjobfradrag
		+ MekstraPensionsfradrag

	form.MligningsmaessigeFradrag.value = tilDanskHeltal(afrund(MligningsmaessigeFradrag))

	KligningsmaessigeFradrag =
		parse(form.Kbefordring.value)
		+ parse(form.Kfagligt.value)
		+ parse(form.KoevrigeLoenmodtagerudgifter.value)
		+ parse(form.Kaegtefaellebidrag.value)
		+ parse(form.KandreLignings.value)
		+ Kbeskaeftigelsesfradrag
		+ Kjobfradrag
		+ KekstraPensionsfradrag

	form.KligningsmaessigeFradrag.value = tilDanskHeltal(afrund(KligningsmaessigeFradrag))
	
	// skattepligtig indkomst
	MskattepligtigIndkomst =
		MpersonligIndkomst
		+ Mkapitalindkomst
		- MligningsmaessigeFradrag

	form.MskattepligtigIndkomst.value = tilDanskHeltal(afrund(MskattepligtigIndkomst))

	KskattepligtigIndkomst =
		KpersonligIndkomst
		+ Kkapitalindkomst
		- KligningsmaessigeFradrag

	form.KskattepligtigIndkomst.value = tilDanskHeltal(afrund(KskattepligtigIndkomst))

	// *************
	// Aktieindkomst
	// *************
	Maktieindkomst =
		parse(form.M61.value)
		+ parse(form.M64.value)

	form.Maktieindkomst.value = tilDanskHeltal(afrund(Maktieindkomst))

	Kaktieindkomst =
		parse(form.K61.value)
		+ parse(form.K64.value)

	form.Kaktieindkomst.value = tilDanskHeltal(afrund(Kaktieindkomst))
	
	return form
}

function skatteberegning(form) {
fatalFejl = false // Hvis sand: Resultatside vises ikke. Variablen er global

// her ved man, at alle oplysninger er (forsøgt) indtastet
// Der er allerede på et tidligere tidspunkt givet advarsel

if (skatteorakel) {
	// Disse fejlmeddelser vises ikke, hvis blot skatteberegning
	if (form.Munder18[0].checked && (form.boern15_17[0].checked || form.boern18_25[0].checked || form.boern26[0].checked)) {
		alert('Du har angivet, at du er under 18 år, men har børn over 15 år!')
		fatalFejl = true
	}
}

// der tillades ikke negativ skattepligtig eller personlig indkomst
if (MpersonligIndkomst < 0 ||
	KpersonligIndkomst < 0) {
		alert("Det forudsættes, at den personlige indkomst er positiv!")
		fatalFejl = true
} else {

	var gift = form.civilstand[0].checked
	// Hvis der er angivet en indkomst under "ægtefælle", er man nok gift -> giv advarsel
	if (!gift && KskattepligtigIndkomst != 0) {
		alert("Du har angivet en indkomst for din ægtefælle, men samtidigt oplyst, at du ikke er gift!")
		fatalFejl = true
	}

	if (!gift && Kaktieindkomst != 0) {
		alert("Du har angivet en aktieindkomst for din ægtefælle, men samtidigt oplyst, at du ikke er gift!")
		fatalFejl = true
	}

/*
	// Hvis man har angivet, at man er gift, men ægtefællen ikke har nogen skattepligtig indkomst,
	// er der nok noget galt -> giv advarsel
	if (gift && KskattepligtigIndkomst == 0) {
		alert("Muligvis mangler der oplysninger! Du har angivet, at du er gift, men din ægtefælles skattepligtige indkomst er 0!")
	}
*/

	var Munder18 = form.Munder18[0].checked
	var Kunder18 = form.Kunder18[0].checked
	var MmedlemFolkekirke = form.MmedlemFolkekirke[0].checked
	var KmedlemFolkekirke = form.KmedlemFolkekirke[0].checked
	
	var i = form.kommune.options.selectedIndex
	kommune(form.kommune.options[i].value,"helaarsbolig")

	// Find grundskyldpromille sommerhus
	i = form.kommuneSommerhus.options.selectedIndex
	kommune(form.kommuneSommerhus.options[i].value,"sommerhus")

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

	form.MpersonfradragKomm.value = tilDanskHeltal((-1) * afrund(Mpersonfradrag))

	if (gift) {
		form.KpersonfradragKomm.value = tilDanskHeltal((-1) * afrund(Kpersonfradrag))
	} else {
		form.KpersonfradragKomm.value = "ugift"
	}

	form.MskattepligtigIndkomstKomm.value = tilDanskHeltal(afrund(MskattepligtigIndkomst))

	MberegningsgrundlagKomm = MskattepligtigIndkomst - Mpersonfradrag
	form.MberegningsgrundlagKomm.value = tilDanskHeltal(afrund(MberegningsgrundlagKomm))

	MkommSkat = MberegningsgrundlagKomm * (MkommSkatprc / 100)
	form.MkommSkat.value = tilDanskHeltal(afrund(MkommSkat))

	form.MkommSkatprc.value = afrund2dec(MkommSkatprc)
	if (gift) {
		form.KkommSkatprc.value = afrund2dec(KkommSkatprc)
	
		form.KskattepligtigIndkomstKomm.value = tilDanskHeltal(afrund(KskattepligtigIndkomst))

		KberegningsgrundlagKomm = KskattepligtigIndkomst - Kpersonfradrag
		form.KberegningsgrundlagKomm.value = tilDanskHeltal(afrund(KberegningsgrundlagKomm))

		KkommSkat = KberegningsgrundlagKomm * (KkommSkatprc / 100)
		form.KkommSkat.value = tilDanskHeltal(afrund(KkommSkat))

		// evt. negativ skat modregnes først i ægtefællens skat, jfr. PSL § 13, stk. 2 og PSL § 10, stk. 3
		kommSkatIalt = MkommSkat + KkommSkat
	} else {
		form.KkommSkatprc.value = "ugift"

		form.KskattepligtigIndkomstKomm.value = "ugift"
		form.KberegningsgrundlagKomm.value = "ugift"
		form.KkommSkat.value = "ugift"

		kommSkatIalt = MkommSkat
	}

	// evt. negativ skat modregnes i øvrige skatter, jfr. PSL §§ 9, stk. 1, og 13, stk. 1
	form.kommSkatIalt.value = tilDanskHeltal(afrund(kommSkatIalt))

	// kommunal skat [slut]

	///////////////////
	// Bundskat
	///////////////////
	// Der tages ikke højde for § 25a og § 27a i personskatteloven, jfr. lovbek. nr. 918 af 4/10-2000
	// Det betyder, at skatten vil kunne være lavere end beregnet her

	form.bundskatprc.value = bundskatprc

	var MberegningsgrundlagBund
	var KberegningsgrundlagBund

	var MpositivKapitalindkomstBund
	var KpositivKapitalindkomstBund

	var Mbundskat
	var Kbundskat
	var bundskatIalt // samlet bundskat

	form.MpersonligIndkomstBund.value = tilDanskHeltal(afrund(MpersonligIndkomst))
	form.MpersonfradragBund.value = tilDanskHeltal((-1) * afrund(Mpersonfradrag))

	if (gift) {
		form.KpersonligIndkomstBund.value = tilDanskHeltal(afrund(KpersonligIndkomst))

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

		form.MpositivKapitalindkomstBund.value = tilDanskHeltal(afrund(MpositivKapitalindkomstBund))
		form.KpositivKapitalindkomstBund.value = tilDanskHeltal(afrund(KpositivKapitalindkomstBund))

		form.KpersonfradragBund.value = tilDanskHeltal((-1) * afrund(Kpersonfradrag))

		MberegningsgrundlagBund =
			MpersonligIndkomst
			+ MpositivKapitalindkomstBund
			- Mpersonfradrag

		KberegningsgrundlagBund =
			KpersonligIndkomst
			+ KpositivKapitalindkomstBund
			- Kpersonfradrag

		form.MberegningsgrundlagBund.value = tilDanskHeltal(afrund(MberegningsgrundlagBund))
		form.KberegningsgrundlagBund.value = tilDanskHeltal(afrund(KberegningsgrundlagBund))

		Mbundskat = MberegningsgrundlagBund * (bundskatprc / 100)
		form.Mbundskat.value = tilDanskHeltal(afrund(Mbundskat))

		Kbundskat = KberegningsgrundlagBund * (bundskatprc / 100)
		form.Kbundskat.value = tilDanskHeltal(afrund(Kbundskat))

		bundskatIalt = Mbundskat + Kbundskat
	} else { // ugift
		MpositivKapitalindkomstBund = pos(Mkapitalindkomst)

		form.MpositivKapitalindkomstBund.value = tilDanskHeltal(afrund(MpositivKapitalindkomstBund))

		MberegningsgrundlagBund =
			MpersonligIndkomst
			+ MpositivKapitalindkomstBund
			- Mpersonfradrag

		form.MberegningsgrundlagBund.value = tilDanskHeltal(afrund(MberegningsgrundlagBund))

		Mbundskat = MberegningsgrundlagBund * (bundskatprc / 100)
		form.Mbundskat.value = tilDanskHeltal(afrund(Mbundskat))

		form.KpersonligIndkomstBund.value = "ugift"
		form.KpositivKapitalindkomstBund.value = "ugift"
		form.KpersonfradragBund.value = "ugift"
		form.KberegningsgrundlagBund.value = "ugift"
		form.Kbundskat.value = "ugift"
	
		bundskatIalt = Mbundskat
	}

	// evt. negativ skat modregnes i øvrige skatter, jfr. PSL §§ 9, stk. 1, og 13, stk. 1
	form.bundskatIalt.value = tilDanskHeltal(afrund(bundskatIalt))

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

	form.topskatprc_personlig_indkomst.value = topskatprcReduceret

	// Topskatteprocent for positiv nettokapitalindkomst reduceres, hvis det skrå skatteloft for positiv nettokapitalindkomst er passeret
	var samletprc = kommuneprc + sundhedsbidragprc + bundskatprc + topskatprc
	var topskatprcReduceret_positivkapitalindkomst

	if (samletprc > skatteloftprc_positivkapitalindkomst) {
		topskatprcReduceret_positivkapitalindkomst = topskatprc - forskelToDecimaler(samletprc,skatteloftprc_positivkapitalindkomst)
	} else {
		topskatprcReduceret_positivkapitalindkomst = topskatprc
	}

	form.topskatprc_positivkapitalindkomst.value = afrund2dec(topskatprcReduceret_positivkapitalindkomst)

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

	form.MpersonligIndkomstTop.value = tilDanskHeltal(afrund(MpersonligIndkomst))
	form.MindskudKapitalpension.value = tilDanskHeltal(afrund(MindskudKapitalpension))
	form.MarbejdsgiverIndskudKapitalpension1.value = tilDanskHeltal(afrund(MarbejdsgiverIndskudKapitalpension))
	form.topskatgraense1.value = tilDanskHeltal((-1) * afrund(topskatgraense))

	var MpersonligIndkomstogIndskudPension = MpersonligIndkomst
		+ MindskudKapitalpension
		+ MarbejdsgiverIndskudKapitalpension;

	if (gift) {
		form.KpersonligIndkomstTop.value = tilDanskHeltal(afrund(KpersonligIndkomst))
		form.KindskudKapitalpension.value = tilDanskHeltal(afrund(KindskudKapitalpension))
		form.KarbejdsgiverIndskudKapitalpension1.value = tilDanskHeltal(afrund(KarbejdsgiverIndskudKapitalpension))

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

			form.MpositivKapitalindkomstTop.value = tilDanskHeltal(afrund(MpositivKapitalindkomstTop))
			form.KpositivKapitalindkomstTop.value = ""

			if (MpersonligIndkomstogIndskudPension >= topskatgraense) {
				var topskatgraense_positivkapitalindkomst = 0;
			} else {
				var topskatgraense_positivkapitalindkomst = topskatgraense - MpersonligIndkomstogIndskudPension;
			}

			form.topskatgraense3.value = tilDanskHeltal((-1) * afrund(topskatgraense_positivkapitalindkomst));
			form.topskatgraense4.value = "";

			// B. Beregning af topskat af positiv nettokapitalindkomst
			var MberegningsgrundlagTop_positivkapitalindkomst = MpositivKapitalindkomstTop - topskatgraense_positivkapitalindkomst;

			form.MberegningsgrundlagTop_positivkapitalindkomst.value = tilDanskHeltal(afrund(MberegningsgrundlagTop_positivkapitalindkomst))
			form.KberegningsgrundlagTop_positivkapitalindkomst.value = "";

			var Mtopskat_positivkapitalindkomst = MberegningsgrundlagTop_positivkapitalindkomst * (topskatprcReduceret_positivkapitalindkomst / 100)
			var Ktopskat_positivkapitalindkomst = 0;

			form.Mtopskat_positivkapitalindkomst.value = tilDanskHeltal(afrund(Mtopskat_positivkapitalindkomst))

			form.Ktopskat_positivkapitalindkomst.value = "";
		} else {
			// beregning på toppen af ægtefællens indkomst
			KpositivKapitalindkomstTop = samlPositivKapitalindkomst
			MpositivKapitalindkomstTop = 0

			form.MpositivKapitalindkomstTop.value = ""
			form.KpositivKapitalindkomstTop.value = tilDanskHeltal(afrund(KpositivKapitalindkomstTop))

			if (KpersonligIndkomstogIndskudPension >= topskatgraense) {
				topskatgraense_positivkapitalindkomst = 0;
			} else {
				topskatgraense_positivkapitalindkomst = topskatgraense - KpersonligIndkomstogIndskudPension;
			}

			form.topskatgraense3.value = "";
			form.topskatgraense4.value = tilDanskHeltal((-1) * afrund(topskatgraense_positivkapitalindkomst));

			// B. Beregning af topskat af positiv nettokapitalindkomst
			var KberegningsgrundlagTop_positivkapitalindkomst = KpositivKapitalindkomstTop - topskatgraense_positivkapitalindkomst;

			form.MberegningsgrundlagTop_positivkapitalindkomst.value = "";
			form.KberegningsgrundlagTop_positivkapitalindkomst.value = tilDanskHeltal(afrund(KberegningsgrundlagTop_positivkapitalindkomst))

			form.Mtopskat_positivkapitalindkomst.value = "";

			Mtopskat_positivkapitalindkomst = 0;
			Ktopskat_positivkapitalindkomst = KberegningsgrundlagTop_positivkapitalindkomst * (topskatprcReduceret_positivkapitalindkomst / 100)

			form.Ktopskat_positivkapitalindkomst.value = tilDanskHeltal(afrund(Ktopskat_positivkapitalindkomst))
		}

		form.topskatgraense1.value = tilDanskHeltal((-1) * afrund(topskatgraense))
		form.topskatgraense2.value = tilDanskHeltal((-1) * afrund(topskatgraense))

		// A. Beregning af topskat af personlig indkomst og indskud på kapitalpension

		MberegningsgrundlagTop_personlig_indkomst = MpersonligIndkomstogIndskudPension
			- topskatgraense

		KberegningsgrundlagTop_personlig_indkomst = KpersonligIndkomstogIndskudPension
			- topskatgraense

		form.MberegningsgrundlagTop_personlig_indkomst.value = tilDanskHeltal(afrund(MberegningsgrundlagTop_personlig_indkomst))
		form.KberegningsgrundlagTop_personlig_indkomst.value = tilDanskHeltal(afrund(KberegningsgrundlagTop_personlig_indkomst))

		var Mtopskat_personlig_indkomst = MberegningsgrundlagTop_personlig_indkomst * (topskatprcReduceret / 100)
		form.Mtopskat_personlig_indkomst.value = tilDanskHeltal(afrund(Mtopskat_personlig_indkomst))

		var Ktopskat_personlig_indkomst = KberegningsgrundlagTop_personlig_indkomst * (topskatprcReduceret / 100)
		form.Ktopskat_personlig_indkomst.value = tilDanskHeltal(afrund(Ktopskat_personlig_indkomst))


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

		form.MpositivKapitalindkomstTop.value = tilDanskHeltal(afrund(MpositivKapitalindkomstTop))

		// A. Beregning af topskat af personlig indkomst og indskud på kapitalpension

		MberegningsgrundlagTop_personlig_indkomst = MpersonligIndkomstogIndskudPension
			- topskatgraense

		form.MberegningsgrundlagTop_personlig_indkomst.value = tilDanskHeltal(afrund(MberegningsgrundlagTop_personlig_indkomst))
		form.KberegningsgrundlagTop_personlig_indkomst.value = "ugift"

		Mtopskat_personlig_indkomst = MberegningsgrundlagTop_personlig_indkomst * (topskatprcReduceret / 100)
		form.Mtopskat_personlig_indkomst.value = tilDanskHeltal(afrund(Mtopskat_personlig_indkomst))
		form.Ktopskat_personlig_indkomst.value = "ugift"

		// B. Beregning af topskat af positiv nettokapitalindkomst

		if (MpersonligIndkomstogIndskudPension >= topskatgraense) {
			topskatgraense_positivkapitalindkomst = 0;
		} else {
			topskatgraense_positivkapitalindkomst = topskatgraense - MpersonligIndkomstogIndskudPension;
		}

		form.topskatgraense3.value = tilDanskHeltal((-1) * afrund(topskatgraense_positivkapitalindkomst));
		form.topskatgraense4.value = "ugift"

		MberegningsgrundlagTop_positivkapitalindkomst = MpositivKapitalindkomstTop
			- topskatgraense_positivkapitalindkomst;

		form.MberegningsgrundlagTop_positivkapitalindkomst.value = tilDanskHeltal(afrund(MberegningsgrundlagTop_positivkapitalindkomst))
		form.KberegningsgrundlagTop_positivkapitalindkomst.value = "ugift";

		Mtopskat_positivkapitalindkomst = MberegningsgrundlagTop_positivkapitalindkomst * (topskatprcReduceret_positivkapitalindkomst / 100)
		Ktopskat_positivkapitalindkomst = 0;

		form.Mtopskat_positivkapitalindkomst.value = tilDanskHeltal(afrund(Mtopskat_positivkapitalindkomst))
		form.Ktopskat_positivkapitalindkomst.value = "";

		form.KpersonligIndkomstTop.value = "ugift"
		form.KindskudKapitalpension.value = "ugift"
		form.KarbejdsgiverIndskudKapitalpension1.value = "ugift"
		form.KpositivKapitalindkomstTop.value = "ugift"
		form.topskatgraense2.value = "ugift"

		form.KberegningsgrundlagTop_positivkapitalindkomst.value = "ugift"
		form.Ktopskat_positivkapitalindkomst.value = "ugift"

		topskatIalt_personlig_indkomst = pos(Mtopskat_personlig_indkomst);
		topskatIalt_positivkapitalindkomst = pos(Mtopskat_positivkapitalindkomst);

		topskatIalt = topskatIalt_personlig_indkomst + topskatIalt_positivkapitalindkomst
	}


	form.bundfradrag_positiv_nettokapitalindkomst.value = tilDanskHeltal(bundfradrag_positiv_nettokapitalindkomst);
	form.topskatIalt_personlig_indkomst.value = tilDanskHeltal(afrund(topskatIalt_personlig_indkomst))
	form.topskatIalt_positivkapitalindkomst.value = tilDanskHeltal(afrund(topskatIalt_positivkapitalindkomst))

	// skat kan kun blive positiv (i.e. kan ikke modregnes)

	form.topskatIalt.value = tilDanskHeltal(afrund(topskatIalt))

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

	var parcelhus = form.bolig[2].checked
	var ejerlejlighed = form.bolig[3].checked
	var senestJuli1998 = form.senestJuli1998[0].checked

	if (parcelhus || ejerlejlighed) {

		ejendomsvaerdi = parse(form.angivetEjendomsvaerdi.value)
		form.ejendomsvaerdi.value = tilDanskHeltal(afrund(ejendomsvaerdi))

		if (ejendomsvaerdi <= ejendomsvaerdigraense) {
			ejendomsvaerdiskatUnder = ejendomsvaerdi * (ejendomsvaerdiskatprcUnder / 100)
			form.ejendomsvaerdiskatUnder.value = tilDanskHeltal(afrund(ejendomsvaerdiskatUnder))
	
			ejendomsvaerdiskatOver = 0	
			form.ejendomsvaerdiskatOver.value = ""
		} else {
			// under grænsen
			ejendomsvaerdiskatUnder = ejendomsvaerdigraense * (ejendomsvaerdiskatprcUnder / 100)
			form.ejendomsvaerdiskatUnder.value = tilDanskHeltal(afrund(ejendomsvaerdiskatUnder))
	
			// over grænsen
			ejendomsvaerdiskatOver = (ejendomsvaerdi - ejendomsvaerdigraense)
				* (ejendomsvaerdiskatprcOver / 100)
			form.ejendomsvaerdiskatOver.value = tilDanskHeltal(afrund(ejendomsvaerdiskatOver))
		}

		nedslag = 0
		if (senestJuli1998) {
			// Jfr. ejendomsværdiskatteloven § 6
			nedslagsprc = 0.2

			nedslag = ejendomsvaerdi * (nedslagsprc / 100)

			if (parcelhus) {
				// nedslag yderligere 0.4 %, dog max. 1.200 kr., jfr. ejendomsværdiskatteloven § 7
				nedslagsprc = 0.4

				nedslag += Math.min(ejendomsvaerdi * (nedslagsprc / 100), 1200)
			}
		} else {
			nedslagsprc = 0
			nedslag = 0
		}

		form.nedslag.value = tilDanskHeltal(afrund(nedslag))

		ejendomsvaerdiskatHelaarsbolig = ejendomsvaerdiskatUnder
			+ ejendomsvaerdiskatOver
			- nedslag

		form.ejendomsvaerdiskatHelaarsbolig.value = tilDanskHeltal(afrund(ejendomsvaerdiskatHelaarsbolig))
	
	} else {
		if (parse(form.angivetEjendomsvaerdi.value) > 0) {
			alert("Du har angivet en ejendomsværdi og samtidigt oplyst, at du har en lejebolig/andelsbolig!")
			fatalFejl = true
		}

		form.ejendomsvaerdi.value = "leje/andelsbolig"
		form.ejendomsvaerdiskatUnder.value = ""
		form.ejendomsvaerdiskatOver.value = ""

		ejendomsvaerdiskatHelaarsbolig = 0
		form.ejendomsvaerdiskatHelaarsbolig.value = ejendomsvaerdiskatHelaarsbolig
	}

	// Sommerhus
	var ejendomsvaerdiSommerhus
	var ejendomsvaerdiskatUnderSommerhus 
	var ejendomsvaerdiskatOverSommerhus
	var ejendomsvaerdiskatSommerhus

	var nedslagsprcSommerhus
	var nedslagSommerhus

	var sommerhus = form.sommerhus[0].checked
	var senestJuli1998Sommerhus = form.senestJuli1998Sommerhus[0].checked

	if (sommerhus) {
		ejendomsvaerdiSommerhus = parse(form.angivetEjendomsvaerdiSommerhus.value)
		form.ejendomsvaerdiSommerhus.value = tilDanskHeltal(afrund(ejendomsvaerdiSommerhus))

		if (ejendomsvaerdiSommerhus <= ejendomsvaerdigraense) {
			ejendomsvaerdiskatUnderSommerhus = ejendomsvaerdiSommerhus * (ejendomsvaerdiskatprcUnder / 100)
			form.ejendomsvaerdiskatUnderSommerhus.value = tilDanskHeltal(afrund(ejendomsvaerdiskatUnderSommerhus))
	
			ejendomsvaerdiskatOverSommerhus = 0	
			form.ejendomsvaerdiskatOverSommerhus.value = ""
		} else {
			// under grænsen
			ejendomsvaerdiskatUnderSommerhus = ejendomsvaerdigraense * (ejendomsvaerdiskatprcUnder / 100)
			form.ejendomsvaerdiskatUnderSommerhus.value = tilDanskHeltal(afrund(ejendomsvaerdiskatUnderSommerhus))
	
			// over grænsen
			ejendomsvaerdiskatOverSommerhus = (ejendomsvaerdiSommerhus - ejendomsvaerdigraense)
				* (ejendomsvaerdiskatprcOver / 100)
			form.ejendomsvaerdiskatOverSommerhus.value = tilDanskHeltal(afrund(ejendomsvaerdiskatOverSommerhus))
		}

		nedslagSommerhus = 0
		if (senestJuli1998Sommerhus) {
			// Jfr. ejendomsværdiskatteloven § 6
			nedslagsprc = 0.2

			nedslagSommerhus = ejendomsvaerdiSommerhus * (nedslagsprc / 100)

			// nedslag yderligere 0.4 %, dog max. 1.200 kr., jfr. ejendomsværdiskatteloven § 7
			nedslagsprc = 0.4

			nedslagSommerhus += Math.min(ejendomsvaerdiSommerhus * (nedslagsprc / 100), 1200)
		} else {
			nedslagsprc = 0
			nedslagSommerhus = 0
		}

		form.nedslagSommerhus.value = tilDanskHeltal(afrund(nedslagSommerhus))

		ejendomsvaerdiskatSommerhus = ejendomsvaerdiskatUnderSommerhus
			+ ejendomsvaerdiskatOverSommerhus
			- nedslagSommerhus

		form.ejendomsvaerdiskatSommerhus.value = tilDanskHeltal(afrund(ejendomsvaerdiskatSommerhus))
	
	} else {
		if (parse(form.angivetEjendomsvaerdiSommerhus.value) > 0) {
			alert("Du har angivet en ejendomsværdi for et sommerhus og samtidigt oplyst, at du ikke har et sommerhus!")
			fatalFejl = true
		}

		form.ejendomsvaerdiSommerhus.value = "intet sommerhus"
		form.ejendomsvaerdiskatUnderSommerhus.value = ""
		form.ejendomsvaerdiskatOverSommerhus.value = ""

		ejendomsvaerdiskatSommerhus = 0
		form.ejendomsvaerdiskatSommerhus.value = ejendomsvaerdiskatSommerhus
	}

	ejendomsvaerdiskatIalt = ejendomsvaerdiskatHelaarsbolig
					+ ejendomsvaerdiskatSommerhus

	form.ejendomsvaerdiskatIalt.value = tilDanskHeltal(afrund(ejendomsvaerdiskatIalt))

	///////////////////////////////////
	// Grundskyld
	///////////////////////////////////
	var grundskyldIalt	
	var grundvaerdi
	var grundskyldHelaarsbolig

	// Helårsbolig

	var parcelhus = form.bolig[2].checked
	var ejerlejlighed = form.bolig[3].checked

	if (parcelhus || ejerlejlighed) {

		grundvaerdi = parse(form.angivetGrundvaerdi.value);
		form.grundvaerdi.value = tilDanskHeltal(afrund(grundvaerdi));

		form.grundskyldpromille.value = grundskyldpromille;

		grundskyldHelaarsbolig = grundvaerdi * grundskyldpromille / 1000;
		form.grundskyldHelaarsbolig.value = tilDanskHeltal(afrund(grundskyldHelaarsbolig));
	} else {
		if (parse(form.angivetGrundvaerdi.value) > 0) {
			alert("Du har angivet en grundværdi og samtidigt oplyst, at du har en lejebolig/andelsbolig!");
			fatalFejl = true;
		}

		form.grundvaerdi.value = "leje/andelsbolig"
		form.grundskyldpromille.value = "";

		grundskyldHelaarsbolig = 0
		form.grundskyldHelaarsbolig.value = grundskyldHelaarsbolig
	}

	// Sommerhus
	var grundvaerdiSommerhus
	var grundskyldSommerhus

	var sommerhus = form.sommerhus[0].checked
	var senestJuli1998Sommerhus = form.senestJuli1998Sommerhus[0].checked

	if (sommerhus) {
		grundvaerdiSommerhus = parse(form.angivetGrundvaerdiSommerhus.value);
		form.grundvaerdiSommerhus.value = tilDanskHeltal(afrund(grundvaerdiSommerhus));

		form.grundskyldpromilleSommerhus.value = grundskyldpromilleSommerhus;

		grundskyldSommerhus = grundvaerdiSommerhus * grundskyldpromilleSommerhus / 1000;
		form.grundskyldSommerhus.value = tilDanskHeltal(afrund(grundskyldSommerhus));

	} else {
		if (parse(form.angivetGrundvaerdiSommerhus.value) > 0) {
			alert("Du har angivet en grundværdi for et sommerhus og samtidigt oplyst, at du ikke har et sommerhus!")
			fatalFejl = true
		}

		form.grundvaerdiSommerhus.value = "intet sommerhus"
		form.grundskyldpromilleSommerhus.value = "";

		grundskyldSommerhus = 0
		form.grundskyldSommerhus.value = grundskyldSommerhus
	}

	grundskyldIalt = grundskyldHelaarsbolig
				+ grundskyldSommerhus

	form.grundskyldIalt.value = tilDanskHeltal(afrund(grundskyldIalt))

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
	
	form.Maktieindkomst1.value = tilDanskHeltal(afrund(Maktieindkomst))
	samletAktieindkomst = Maktieindkomst

	form.Maktiegraense.value = tilDanskHeltal(afrund(aktieskatgrundbeloeb))
	samletProgressionsgraense = aktieskatgrundbeloeb

	if (gift) {
		form.Kaktieindkomst1.value = tilDanskHeltal(afrund(Kaktieindkomst))
		samletAktieindkomst += Kaktieindkomst

		form.Kaktiegraense.value = tilDanskHeltal(afrund(aktieskatgrundbeloeb))
		samletProgressionsgraense += aktieskatgrundbeloeb

	} else {
		form.Kaktieindkomst1.value = "ugift"
		form.Kaktiegraense.value = "ugift"
	}

	form.samletAktieindkomst.value = tilDanskHeltal(afrund(samletAktieindkomst))
	form.samletProgressionsgraense.value = tilDanskHeltal(afrund(samletProgressionsgraense))

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

	form.aktieindkomstUnderGraense.value = tilDanskHeltal(afrund(aktieindkomstUnderGraense))
	form.aktieindkomstOverGraense.value = tilDanskHeltal(afrund(aktieindkomstOverGraense))

	aktieskatUnderGraense = aktieindkomstUnderGraense * (underAktieskatprc / 100) 
	aktieskatOverGraense = aktieindkomstOverGraense * (overAktieskatprc / 100) 

	form.aktieskatUnderGraense.value = tilDanskHeltal(afrund(aktieskatUnderGraense))
	form.aktieskatOverGraense.value = tilDanskHeltal(afrund(aktieskatOverGraense))

	aktieskatIalt = aktieskatUnderGraense + aktieskatOverGraense
	
	form.aktieskatIalt.value = tilDanskHeltal(afrund(aktieskatIalt))

	form.aktieskatprcUnderGraense.value = underAktieskatprc
	form.aktieskatprcOverGraense.value = overAktieskatprc

	// aktieskat [slut]

	//////////////////////////////////
	// AMB og ATP-bidrag
	//////////////////////////////////

	// beregningen er foretaget oven for i indkomstopgørelse
	form.AMBATPprc.value = AMBprc

	var MberegningsgrundlagAMB
	var KberegningsgrundlagAMB
	var AMBIalt

	form.MloenFoerAMB.value = tilDanskHeltal(afrund(MloenFoerAMB))

	MberegningsgrundlagAMB = MloenFoerAMB
	form.MberegningsgrundlagAMB.value = tilDanskHeltal(afrund(MberegningsgrundlagAMB))

	form.MAMB.value = tilDanskHeltal(afrund(MAMB))

	if (gift) {
		form.KloenFoerAMB.value = tilDanskHeltal(afrund(KloenFoerAMB))

		KberegningsgrundlagAMB = KloenFoerAMB
		form.KberegningsgrundlagAMB.value = tilDanskHeltal(afrund(KberegningsgrundlagAMB))
		
		form.KAMB.value = tilDanskHeltal(afrund(KAMB))

		AMBIalt = MAMB + KAMB
	} else {
		form.KloenFoerAMB.value = "ugift"
		form.KAMB.value = "ugift"
		form.KberegningsgrundlagAMB.value = "ugift"

		AMBIalt = MAMB
	}

	form.AMBIalt.value = tilDanskHeltal(afrund(AMBIalt))
	// AMB og ATP-bidrag [slut]

// ** Start: Ny 2012 ****

	///////////////////////////////////////
	// Nedslag negativ nettokapitalindkomst
	///////////////////////////////////////

	// Jf. personskattelovens § 11

	var nedslagsgraenseNegativKapitalindkomst;

	form.nedslagNegativNettokapitalindkomstprc.value = nedslagNegativNettokapitalindkomstprc

	form.Mkapitalindkomst_nedslag.value = tilDanskHeltal(afrund(Mkapitalindkomst));
	if (gift) {
		nedslagsgraenseNegativKapitalindkomst = 2 * 50000;
		form.Kkapitalindkomst_nedslag.value = tilDanskHeltal(afrund(Kkapitalindkomst));
	} else {
		nedslagsgraenseNegativKapitalindkomst = 50000;
		form.Kkapitalindkomst_nedslag.value = "ugift";
	}

	if (Mkapitalindkomst + Kkapitalindkomst < 0) {
		var SamletNegativKapitalindkomst_nedslag = (-1)*(Mkapitalindkomst + Kkapitalindkomst);

		if (SamletNegativKapitalindkomst_nedslag > nedslagsgraenseNegativKapitalindkomst) {
			SamletNegativKapitalindkomst_nedslag = nedslagsgraenseNegativKapitalindkomst;
		}
	} else {
		SamletNegativKapitalindkomst_nedslag = 0;
	}

	form.SamletNegativKapitalindkomst_nedslag.value = tilDanskHeltal(afrund((-1)*SamletNegativKapitalindkomst_nedslag));

	var NedslagNegativKapitalindkomst;

	NedslagNegativKapitalindkomst = SamletNegativKapitalindkomst_nedslag * (nedslagNegativNettokapitalindkomstprc/100);
	
	form.NedslagNegativKapitalindkomst.value =  tilDanskHeltal(afrund((-1)*NedslagNegativKapitalindkomst));

	form.IaltNedslagNegativKapitalindkomst.value = tilDanskHeltal(afrund((-1)*NedslagNegativKapitalindkomst));

	// Nedslag negativ nettokapitalindkomst [slut]

// ** Slut: Ny 2012 ****

	// Samlet skat inkl. AMB og ATP-bidrag
	skatIalt = 
		// negativ kommunal skat og bundskat kan modregnes i mellem- og topskat og i aktieskat over mellem- og topgrænse
		pos(kommSkatIalt
				+ bundskatIalt
				+ topskatIalt
				+ aktieskatOverGraense
				- NedslagNegativKapitalindkomst)

		// skat efter § 8 a, stk. 1, er endelig - ikke modregning af ovenstående i skatten
	skatIalt += aktieskatUnderGraense

		// der kan ikke modregnes i ejendomsværdiskat og arbejdsmarkedsbidrag
	skatIalt = pos(skatIalt)
			+ AMBIalt 

	form.skatIalt.value = tilDanskHeltal(afrund(skatIalt))


	var skatFastEjendomIalt = ejendomsvaerdiskatIalt + grundskyldIalt;
	form.skatFastEjendomIalt.value = tilDanskHeltal(afrund(skatFastEjendomIalt))

}
}

// Hjælpefunktioner
function forskelEenDecimal(x, y) {
	// returnerer x-y med en decimal
	return (Math.round(x*10 - y*10) / 10)
}

function forskelToDecimaler(x, y) {
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

function parse(str) {
	return parse3(str)
}

function parse3(str) {
	// Læser kun heltal
	let resultat = parseInt(str)

	if (isNaN(resultat)) {
		return 0
	} else {
		return resultat
	}
}

function tilDanskHeltal (heltal) {
	// Funktionen returnerer en streng som repræsenterer tallet heltal med eventuelle punktummer som 1000-tals-adskillelse
	// Eksempel:
	// tilDanskHeltal(1000000) = "1.000.000"
	// tilDanskHeltal(-1000) = "-1.000"
	// Undersøg om tallet er negativt
	
	let neg;
	
	if (heltal < 0) {
		heltal = (-1) * heltal
		neg = "-"
	} else {
		neg = ""
	}

	let str = ""

	let cifferplads=0
	let rest = heltal
	while (rest >= 10) {
		cifferplads++
		str = (rest % 10) + str
		if (cifferplads == 3) {
			cifferplads = 0
			str = "." + str
		}
		rest = (rest - (rest % 10)) / 10
	}
	// sidste ciffer
	str = rest + str
	return neg + str
}

function talkontrol(str) {
	// Kontrollerer, at der i str ikke forekommer . eller ,
	if (str.indexOf(",") != -1) {
		alert("Fejl i sidste tal: Kun hele tal. Brug ikke komma (,) i talangivelser.")
	}

	if (str.indexOf(".") != -1) {
		alert("Fejl i sidste tal: Brug ikke punktum (.) i talangivelser.")
	}

	// Kontrollerer, at der ikke er negative tal
	if (str.indexOf("-") != -1) {
		alert("Fejl i sidste tal: Indtast kun positive tal.")
	}
}

function ingenUdfyldning() {
	alert("Du skal ikke indtaste noget i dette felt!")
}

function onlyNumbers(e) {
	// Kun tal
	var keynum;
	var keychar;
	var numcheck;

	if(window.event) { // IE 
		keynum = e.keyCode;
	} else {
		if (!e.which) return; // Korrektion for fejl i visse browsere

		if(e.which) { // Netscape/Firefox/Opera
		  	keynum = e.which;
		}
	}

	keychar = String.fromCharCode(keynum);
	numcheck = /\d/;

	if (keynum==8) { // backspace
		return true;
	} else {
		return numcheck.test(keychar);
	}
}

function onlyPositiveAndNegativeNumbers(e) {
	// Kun tal og -
	var keynum;
	var keychar;
	var numcheck;

	if(window.event) { // IE 
		keynum = e.keyCode;
	} else {
		if (!e.which) return; // Korrektion for fejl i visse browsere

		if(e.which) { // Netscape/Firefox/Opera
		  	keynum = e.which;
		}
	}

	keychar = String.fromCharCode(keynum);
	numcheck = /\d/;

	if ((keynum==8) || (keynum==45)) { // backspace eller -
		return true;
	} else {
		return numcheck.test(keychar);
	}
}

function noInput(e) {
	return false;
}"""

import re
res = re.findall(pattern=r'form\..+\.value',string=form)



print(set(res))

result = []
for item in set(res):
    r = item.replace('.value',"")
    r = r.replace('form.',"")
    result.append(f"{r}?: number")

print ("\n".join(result))

#
# fixed_tax = re.sub(pattern=r'(\.value)',string=form,repl='')
#
# with open('tax.ts','w') as f:
#     f.write(fixed_tax)