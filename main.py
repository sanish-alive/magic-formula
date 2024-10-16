from flask import Flask, redirect, request, render_template
import webScraping
import MagicFormula

app = Flask(__name__)

route = {
    'open-ipo': '/open-ipo',
    'magic-formula': '/magic-formula'
}

@app.errorhandler(404)
def notFound(e):
    return "<center><h1>404<br>Page Not Found</h1></center>"

@app.route("/")
def home():
    return redirect(route['open-ipo'])

@app.route(route['open-ipo'])
def openIpo():
    data = webScraping.openIPO()
    return render_template("openipo.html", ipo=data)

@app.route(route['magic-formula'], methods=['GET', 'POST'])
def magicFormulaForm():
    if request.method == 'POST':
        companies = {}
        # Iterate over form keys
        for key in request.form.keys():
            if key.endswith('_symbol'):
                # Extract the company name from the key
                selected_company = key.replace('_symbol', '')

                # Process the data for the selected company
                net_income = request.form.get(f'{selected_company}_netincome')
                total_asset = request.form.get(f'{selected_company}_totalasset')

                companies[selected_company] = {
                    "netIncome": float(net_income),
                    "totalAsset": float(total_asset)
                }
        print(companies)
        data = MagicFormula.dataExtraction(companies)
        return render_template("magictable.html", data=data)
        #return data
    elif request.method == 'GET':
        stock = ["USHL", "ACLBSL", "ACLBSLP", "ANLB", "ANLBP", "ACEDPO", "ADBL", "ADBLD83", "ADBLB", "ADBLB86", "ADBLB87", "ALDBLP", "AKJCL", "APEXPO", "API", "ARDBLP", "AKPL", "AHPC", "AVU", "ALBSL", "ALBSLP", "AHL", "ALICLP", "ALICL", "AVYANP", "AVYAN", "BBBLNP", "BGDBLP", "BHL", "BOKD86KA", "BOKD2079", "BOKD86", "BHPL", "BARUN", "BFC", "BFCPO", "BGWT", "BFCLPO", "BEDC", "BHDC", "BSL", "BLDBLP", "BBC", "BNL", "BNT", "BPWP", "BPW", "BNHC", "BUDBLP", "BPCL", "BSM", "CMB", "CMF2", "CHDC", "CFCL", "CFCLPO", "CCBD88", "CGH", "CBBLPO", "CBBL", "CHL", "CHCL", "CIT", "CLI", "CLIP", "CZBILP", "CZBIL", "CMF1", "C30MF", "CIZBD86", "CITY", "PSDBLP", "CBLD88", "CEDBLP", "CORBL", "CORBLP", "CSDBLP", "CNDBLP", "CFL", "CYCL", "CYCLP", "DDBL", "DDBLPO", "DLBS", "DHPL", "DOLTI", "DORDI", "EHPL", "EKBLPO", "ENL", "ENLP", "EBLD85", "EBLD86", "EBLEB89", "EBL", "EBLPO", "EFLPO", "EDBL", "EDBLPO", "FMDBLP", "FMDBL", "FHL", "FOWAD", "FOWADP", "GMFBS", "GMFBSP", "GBBL", "GBBLPO", "GBBD85", "GABLPO", "GHL", "GCIL", "GIBF1", "GBIMEP", "GBIME", "GBD80/81", "GBILD86/87", "GBILD84/85", "GILBPO", "GILB", "GFCL", "GFCLPO", "GWFD83", "GRU", "GBLBSP", "GBLBS", "PDBLPO", "GRANDP", "GRDBL", "GRDBLP", "GVL", "GLH", "GMFILP", "GMFIL", "GLBSL", "GUFL", "GUFLPO", "HAMAPO", "HBT", "HATHY", "HDHPC", "HURJA", "HBLD86", "HBLD83", "HBL", "HBLPO", "HDL", "HEI", "HEIP", "HFL", "HHL", "HLBSLP", "HLBSL", "HLIPO", "HLI", "HPPL", "HIDCL", "HIDCLP", "ILI", "ILIP", "ICFCPO", "ICFC", "ICFCD83", "IGI", "IGIPO", "ILBS", "ILBSP", "IDBLPO", "IHL", "INDBPO", "INDBLP", "JALPA", "JALPAP", "JFL", "JFLPO", "JSLBBP", "JSLBB", "JBLBP", "JBLB", "JHBLPO", "JOSHI", "JBBD87", "JBBL", "JBBLPO", "JSM", "KKBLPO", "KMCDB", "KMCDBP", "KPCL", "KDL", "KDLP", "KCDBLP", "KSBBLD87", "KSBBL", "KSBBLP", "KRBL", "KRBLPO", "KAFILP", "KDBLPO", "KKHC", "KLBSL", "KLBSLP", "KBLPO", "KBL", "KBLD89", "KDBY", "KBLD86", "KEF", "KBSH", "LUK", "LLBSPO", "LLBS", "SFMF", "LBLD86", "LBLD88", "LVF2", "LSL", "LSLPO", "LEMF", "LEC", "LICN", "LICNPO", "LUBLPO", "LBBL", "LBBLPO", "LBBLD89", "LFLCPO", "MBLPO", "MBL", "MBLD87", "MBLD2085", "MBJC", "MFLPO", "MBBLPO", "MLBLD89", "MLBL", "MDBLPO", "MLBLPO", "MLBSL", "MSLB", "MSLBP", "MKHL", "MKJC", "MAKAR", "MEHL", "MKLB", "MKLBP", "MSBBLP", "MHL", "MANDU", "MFILPO", "MFIL", "MFLD85", "MLBS", "MLBSP", "MMKJL", "MKHC", "MMF1", "MCHL", "MERO", "MEROPO", "MSHL", "MMFDBP", "MMFDB", "MDB", "MDBPO", "MLBBL", "MLBBLP", "MEL", "MHCL", "MMDBLP", "MEN", "MHNL", "MND84/85", "MNBBLP", "MNBBL", "MPFLPO", "MPFL", "NABIL", "NABILP", "NBF2", "NBLD82", "NBF3", "NBLD85", "NADEP", "NADEPP", "NBSLPO", "NABBCP", "NABBC", "NNFCPO", "NMFBS", "NMFBSP", "NHPC", "NLICL", "NLICLP", "NILPO", "NIL", "NABBPO", "NBBD2085", "NBLD87", "NBL", "NBBU", "NCCD86", "NTC", "NEFLPO", "NFD", "NFS", "NFSPO", "NHDL", "NIFRA", "NIFRAUR85/86", "NICL", "NICLPO", "NIBD84", "NIBSF2", "NIBD2082", "NIMB", "NIMBPO", "NIBLPF", "NKU", "NLIC", "NLICP", "NLO", "NRIC", "NRM", "SBIPO", "SBI", "SBIBD86", "SBID83", "SBID89", "NSM", "NSMPO", "NTL", "NVG", "NWC", "NLBBL", "NLBBLP", "NESDO", "NESDOP", "NGPL", "NIBLGF", "NICAD8182", "NICD83/84", "NICAD8283", "NICFC", "NICD88", "NICGF", "NICAD 85/86", "NICA", "NICAP", "NICBF", "NICSF", "NICLBSL", "NICLBSLP", "NCMPO", "NUBL", "NUBLPO", "NLG", "NLGPO", "NMBMF", "NMBMFP", "NMBPO", "NMB", "NMBD2085", "NMBD87/88", "NMBEB92/93", "NMBUR93/94", "NMBD89/90", "NMB50", "NSIF2", "NRN", "NYADI", "OFLPO", "OHL", "PADBLP", "PMHPL", "PPCL", "PFCPO", "PFLBSP", "PHCL", "PPL", "PFL", "PFLPO", "PRFLPO", "PRVU", "PRVUPO", "PBLD86", "PBLD84", "PSF", "PBLD87", "PRSF", "PRIN", "PRINPO", "PLI", "PBD85", "PBD88", "PBD84", "PCBL", "PCBLP", "PRDBLP", "PROFLP", "PROFL", "PFILPO", "RADHI", "RJM", "RHGCL", "RBBBLP", "RBBD83", "RBCLPO", "RBCL", "RHPL", "RAWA", "RMF1", "RMF2", "REDBLP", "RNLI", "RNLIP", "RLFL", "RLFLPO", "RIDI", "RFPL", "RSDC", "RSDCP", "RURU", "SABSL", "SABSLPO", "SDLBSL", "SDLBSLP", "SAFLPO", "SMJC", "SALICOPO", "SALICO", "SAHAS", "SAJHAP", "STC", "SAMAJ", "SAMAJP", "SMATA", "SMATAP", "SFC", "SPC", "SFCL", "SFCLP", "SLBSL", "SLBSLPO", "SKBBLP", "SKBBL", "SANIMA", "SNMAPO", "SAND2085", "SAEF", "SBD89", "SBD87", "SLCF", "SGIC", "SGICP", "SAGF", "SHPC", "TAMOR", "SRLI", "SRLIP", "SJCL", "SAPDBL", "SAPDBLP", "SPHL", "SETIPO", "SEWAPO", "SADBL", "SADBLP", "SDBD87", "SICLPO", "SICL", "SHINEP", "SHINE", "SSHL", "SHIVM", "SBPP", "SIFCPO", "SIFC", "SRS", "SHLB", "SHLBP", "SPL", "SFLPO", "SBLD84", "SBLD2082", "SBLD83", "SIGS2", "SBLD89", "SIGS3", "SBL", "SBLPO", "SEF", "SEOS", "SDBLPO", "SPIL", "SPILPO", "SIKLES", "SINDUP", "SINDU", "SHEL", "SHL", "SODBLP", "SONA", "SCBPO", "SCB", "SCBD", "SUBBLP", "SNLI", "SNLIP", "SRBLD83", "SRD80", "SBCF", "SFEF", "SMHL", "SMH", "SMB", "SMBPO", "SUPRMP", "SJLIC", "SJLICP", "SWMF", "SWMFPO", "SWBBLP", "SWBBL", "SMFBS", "SMFBSP", "SLBBLP", "SLBBL", "SGHC", "SPDL", "TRH", "TPC", "TSHL", "TDBLPO", "TBBLP", "UNL", "UFCLPO", "UNHPL", "UFILPO", "UNLBP", "UNLB", "UAILPO", "UAIL", "UMRH", "UMHL", "UPCL", "USLB", "USLBP", "ULBSL", "ULBSLPO", "UHEWA", "ULHC", "USHEC", "UPPER", "VLBS", "VLBSPO", "WNLB", "WNLBP", "YHL"]
        return render_template("magicform.html", stock = stock)
    
    else:
        return "<center><h1>Request Method Wrong</h1></center>"

if __name__ == '__main__':
    app.run(debug=True)

application = app