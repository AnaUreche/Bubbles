//Maya ASCII 2020 scene
//Name: Texture.ma
//Last modified: Wed, May 06, 2020 10:40:19 PM
//Codeset: 1252
requires maya "2020";
requires "stereoCamera" "10.0";
requires "mtoa" "4.0.0";
currentUnit -l centimeter -a degree -t pal;
fileInfo "application" "maya";
fileInfo "product" "Maya 2020";
fileInfo "version" "2020";
fileInfo "cutIdentifier" "201911140446-42a737a01c";
fileInfo "osv" "Microsoft Windows 10 Technical Preview  (Build 18362)\n";
fileInfo "UUID" "D5CD85F1-4F82-C5C6-3897-5EA70EB0931D";
fileInfo "license" "student";
createNode blinn -n "Water";
	rename -uid "73CB870A-48D9-F8A7-0DC6-809B33C68A15";
	setAttr ".rfi" 3;
	setAttr ".rfc" yes;
createNode ramp -n "Texture:RampIncandescence";
	rename -uid "7ECF398A-4B22-36DF-85A6-D999C0860C8C";
	setAttr -s 2 ".cel";
	setAttr ".cel[0].ep" 0;
	setAttr ".cel[0].ec" -type "float3" 0 0 0 ;
	setAttr ".cel[1].ep" 1;
	setAttr ".cel[1].ec" -type "float3" 0 0.0027999999 0.037900001 ;
createNode samplerInfo -n "Texture:samplerInfo1";
	rename -uid "6B625ED5-42AF-6C78-7815-1A975ED70841";
createNode place2dTexture -n "Texture:place2dTexture1";
	rename -uid "A3F3DF22-4024-477A-FA62-AFBC888F04C9";
createNode ramp -n "Texture:RampColor";
	rename -uid "8E3CFBDB-432C-9C0C-775C-D1878E900659";
	setAttr -s 2 ".cel";
	setAttr ".cel[0].ep" 0;
	setAttr ".cel[0].ec" -type "float3" 0 0 0 ;
	setAttr ".cel[1].ep" 1;
	setAttr ".cel[1].ec" -type "float3" 1 1 1 ;
createNode place2dTexture -n "Texture:place2dTexture2";
	rename -uid "37C3F7AC-4C7A-6530-EBF3-A8B502333EC6";
createNode ramp -n "Texture:RampTransparency";
	rename -uid "7DCC025B-4261-B0AE-5D47-AB8071BA2BD9";
	setAttr -s 2 ".cel";
	setAttr ".cel[0].ep" 0;
	setAttr ".cel[0].ec" -type "float3" 0 0 0 ;
	setAttr ".cel[1].ep" 1;
	setAttr ".cel[1].ec" -type "float3" 1 1 1 ;
createNode place2dTexture -n "Texture:place2dTexture3";
	rename -uid "209EF628-4C14-673B-DE08-3180C526EF56";
select -ne :time1;
	setAttr ".o" 186;
	setAttr ".unw" 186;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr ".fprt" yes;
select -ne :renderPartition;
	setAttr -s 8 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 7 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderUtilityList1;
	setAttr -s 20 ".u";
select -ne :defaultRenderingList1;
select -ne :defaultTextureList1;
	setAttr -s 15 ".tx";
select -ne :initialShadingGroup;
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultRenderGlobals;
	setAttr ".ren" -type "string" "arnold";
select -ne :defaultResolution;
	setAttr ".pa" 1;
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
connectAttr "Texture:RampIncandescence.oc" "Water.ic";
connectAttr "Texture:RampColor.oc" "Water.c";
connectAttr "Texture:RampTransparency.oc" "Water.it";
connectAttr "Texture:samplerInfo1.fr" "Texture:RampIncandescence.v";
connectAttr "Texture:place2dTexture1.ou" "Texture:RampIncandescence.u";
connectAttr "Texture:place2dTexture1.ofs" "Texture:RampIncandescence.fs";
connectAttr "Texture:samplerInfo1.fr" "Texture:RampColor.v";
connectAttr "Texture:place2dTexture2.ou" "Texture:RampColor.u";
connectAttr "Texture:place2dTexture2.ofs" "Texture:RampColor.fs";
connectAttr "Texture:samplerInfo1.fr" "Texture:RampTransparency.v";
connectAttr "Texture:place2dTexture3.ou" "Texture:RampTransparency.u";
connectAttr "Texture:place2dTexture3.ofs" "Texture:RampTransparency.fs";
connectAttr "Water.msg" ":defaultShaderList1.s" -na;
connectAttr "Texture:place2dTexture1.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Texture:samplerInfo1.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Texture:place2dTexture2.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Texture:place2dTexture3.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "Texture:RampIncandescence.msg" ":defaultTextureList1.tx" -na;
connectAttr "Texture:RampColor.msg" ":defaultTextureList1.tx" -na;
connectAttr "Texture:RampTransparency.msg" ":defaultTextureList1.tx" -na;
// End of Texture.ma
