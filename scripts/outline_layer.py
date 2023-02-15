from krita import *

K = Krita.instance()
D = K.activeDocument()
N = D.activeNode()


############
# Settings #
############

Color = {
'R': 0,
'G': 0,
'B': 0,
} # Color for lines 0-255

opacity = 50 # 0-100

choke = 100 # 0-100

outline_size = 4


################
# ASL template #
################

asl = '<asl>'\
' <node type="Descriptor" name="" classId="null">'\
'  <node type="UnitFloat" key="Scl " unit="#Prc" value="100"/>'\
'  <node type="Boolean" key="masterFXSwitch" value="1"/>'\
'  <node type="Descriptor" name="" key="IrGl" classId="IrGl">'\
'   <node type="Boolean" key="enab" value="1"/>'\
'   <node type="Enum" typeId="BlnM" key="Md  " value="Mltp"/>'\
'   <node type="Descriptor" name="" key="Clr " classId="RGBC">' +\
\
'    <node type="Double" key="Rd  " value="' + str(Color['R']) + '"/>'\
'    <node type="Double" key="Grn " value="' + str(Color['G']) + '"/>'\
'    <node type="Double" key="Bl  " value="' + str(Color['B']) + '"/>' +\
\
'   </node>' +\
\
'   <node type="UnitFloat" key="Opct" unit="#Prc" value="' + str(opacity) + '"/>' +\
\
'   <node type="Enum" typeId="BETE" key="GlwT" value="SfBL"/>' +\
\
'   <node type="UnitFloat" key="Ckmt" unit="#Pxl" value="' + str(choke) +'"/>' +\
\
'   <node type="UnitFloat" key="blur" unit="#Pxl" value="' + str(outline_size) + '"/>' +\
\
'   <node type="UnitFloat" key="ShdN" unit="#Prc" value="0"/>'\
'   <node type="UnitFloat" key="Nose" unit="#Prc" value="0"/>'\
'   <node type="Boolean" key="AntA" value="0"/>'\
'   <node type="Enum" typeId="IGSr" key="glwS" value="SrcE"/>'\
'   <node type="Descriptor" name="" key="TrnS" classId="ShpC">'\
'    <node type="Text" key="Nm  " value="Linear"/>'\
'    <node type="List" key="Crv ">'\
'     <node type="Descriptor" name="" classId="CrPt">'\
'      <node type="Double" key="Hrzn" value="0"/>'\
'      <node type="Double" key="Vrtc" value="0"/>'\
'     </node>'\
'     <node type="Descriptor" name="" classId="CrPt">'\
'      <node type="Double" key="Hrzn" value="255"/>'\
'      <node type="Double" key="Vrtc" value="255"/>'\
'     </node>'\
'    </node>'\
'   </node>'\
'   <node type="UnitFloat" key="Inpr" unit="#Prc" value="100"/>'\
'  </node>'\
' </node>'\
' <node type="Descriptor" name="" classId="Styl">'\
'  <node type="Descriptor" name="" key="documentMode" classId="documentMode"/>'\
' </node>'\
'</asl>'


def create_layer_with_style(style: str = asl):
    #print(N.layerStyleToAsl())
    parent = N.parentNode()
    new_node = D.createNode("Paint Layer", "paintlayer")
    b = new_node.setLayerStyleFromAsl(style)
    print(b)
    parent.addChildNode(new_node, N)
    

#print(asl_01)
create_layer_with_style()
