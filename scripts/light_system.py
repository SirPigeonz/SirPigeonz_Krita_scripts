from krita import *
from PyQt5.QtCore import QByteArray

K = Krita.instance()
D = K.activeDocument()
N = D.activeNode()


class LightSystem:
    """
    Creates Light System layer structure. After LS creation it can create
    LS Agents layer structures that are using the system to generate light
    effect for shapes in the same group under them.
    """
    
    
    def __init__(self) -> None:
        self.init_light_system()
    
    
    def is_light_system_initialized(self) -> bool:
        root = D.rootNode()
        if D.nodeByName(self._ls_name):
            print("Light System exists.")
            return True
        else:
            print("Light System doesn't exists.")
            return False
    
    
    def init_light_system(self) -> None:
        if not self.is_light_system_initialized():
            print("Lets Initialize!")
            root = D.rootNode()
            
            # Create Light System main group.
            ls_group = D.createGroupLayer(self._ls_name)
            
            # Crteate initial pixel data for layers.
            pixels = D.pixelData(0, 0, D.width(), D.height())
            
            pixel_buffer_black = QByteArray()
            for p in range(0, pixels.size(), 4):
                pixel_buffer_black.append(QByteArray.fromHex(b'000000ff'))
                
            pixel_buffer_white = QByteArray()
            for p in range(0, pixels.size(), 4):
                pixel_buffer_white.append(QByteArray.fromHex(b'ffffffff'))
            
            pixel_buffer_grey = QByteArray()
            for p in range(0, pixels.size(), 4):
                pixel_buffer_grey.append(QByteArray.fromHex(b'7f7f7fff'))
            
            pixel_buffer_blue = QByteArray()
            for p in range(0, pixels.size(), 4):
                pixel_buffer_blue.append(QByteArray.fromHex(b'cb8635ff'))
            
            # FIXME Transparency Mask creation is broken in Krita fix it :/
            selection_50p = Selection()
            selection_50p.select(0, 0, D.width(), D.height(), 128)
            
            # Create layers.
            main_light = light = D.createNode(self._main_light_name, 'paintlayer')
            rim_light = D.createNode(self._rim_light_name, 'paintlayer')
            bounce_light = D.createNode(self._bounce_light_name, 'paintlayer')
            ambient_tint = D.createNode(self._ambient_tint_name, 'paintlayer')
            ambient_lighten = D.createNode(self._ambient_lighten_name, 'paintlayer')
            ambient_darken = D.createNode(self._ambient_darken_name, 'paintlayer')
            
            # Setup layers pixel data.
            main_light.setPixelData(pixel_buffer_grey, 0, 0, D.width(), D.height())
            rim_light.setPixelData(pixel_buffer_grey, 0, 0, D.width(), D.height())
            bounce_light.setPixelData(pixel_buffer_grey, 0, 0, D.width(), D.height())
            ambient_tint.setPixelData(pixel_buffer_blue, 0, 0, D.width(), D.height())
            ambient_lighten.setPixelData(pixel_buffer_black, 0, 0, D.width(), D.height())
            ambient_darken.setPixelData(pixel_buffer_white, 0, 0, D.width(), D.height())
            
            # Setup layers blending modes it's not really needed
            # but serves as reminder what mode is used in Agents.
            main_light.setBlendingMode("dodge")
            rim_light.setBlendingMode("dodge")
            bounce_light.setBlendingMode("dodge")
            ambient_tint.setBlendingMode("hue")
            ambient_lighten.setBlendingMode("screen")
            ambient_darken.setBlendingMode("multiply")
            
            # Setup layers opacity to 0 so it will be easier
            # to select shapes and masks with layer picker.
            main_light.setOpacity(0)
            rim_light.setOpacity(0)
            bounce_light.setOpacity(0)
            ambient_tint.setOpacity(0)
            ambient_lighten.setOpacity(0)
            ambient_darken.setOpacity(0)
            
            #################################################################
            # FIXME Transparency Mask creation is broken in Krita fix it :/ #
            #################################################################
            
            # Create layers opacity masks (yes opacity not transparency).
#            ambient_tint_mask = D.createNode("Ambient Tint Mask", 'transparencymask')
#            ambient_lighten_mask = D.createNode("Ambient Lighten Mask", 'transparencymask')
#            ambient_darken_mask = D.createNode("Ambient Darken Mask", 'transparencymask')
            
            # Set pixel data for masks
            #TransparencyMask(ambient_tint_mask).setSelection(selection_50p)
            
            # Setup layers masks
#            ambient_tint.addChildNode(ambient_tint_mask, None)
#            ambient_lighten.addChildNode(ambient_lighten_mask, None)
#            ambient_darken.addChildNode(ambient_darken_mask, None)
            
            # Add layers to LS Group
            ls_group.addChildNode(ambient_darken, None)
            ls_group.addChildNode(ambient_lighten, ls_group.childNodes()[-1])
            ls_group.addChildNode(ambient_tint, ls_group.childNodes()[-1])
            ls_group.addChildNode(bounce_light, ls_group.childNodes()[-1])
            ls_group.addChildNode(rim_light, ls_group.childNodes()[-1])
            ls_group.addChildNode(main_light, ls_group.childNodes()[-1])
            
            root.addChildNode(ls_group, root.childNodes()[-1])
        else:
            return
    
    
    def find_ls_nodes(self) -> None:
        self._light_system = D.nodeByName(self._ls_name)
        
        self._main_light = D.nodeByName(self._main_light_name)
        self._rim_light = D.nodeByName(self._rim_light_name)
        self._bounce_light = D.nodeByName(self._bounce_light_name)
        self._ambient_tint = D.nodeByName(self._ambient_tint_name)
        self._ambient_lighten = D.nodeByName(self._ambient_lighten_name)
        self._ambient_darken = D.nodeByName(self._ambient_darken_name)
    
    
    def setup_ls_agent(self) -> None:
        print("Create LS Shape")

        parent = N.parentNode()

        # Crteate initial pixel data for layers.
        pixels = D.pixelData(0, 0, D.width(), D.height())
        pixel_buffer_red = QByteArray()
        for p in range(0, pixels.size(), 4):
            pixel_buffer_red.append(QByteArray.fromHex(b'9a0044ff'))
        
        # Guard form adding Agent to LS itself
        if N.name() == self._ls_name:
            return

        # Find Light System Nodes
        self.find_ls_nodes()

        # Create top level LS_Shape
        ls_shape = D.createGroupLayer("LS_Shape")

        # Create LS Agent group.
        agent_group = D.createGroupLayer("LS Agent")
        agent_group.setPassThroughMode(True)
        
        # Create LS layers Sculpt groups.
        main_light_sculpt = D.createGroupLayer(self._main_light_name + " Sculpt")
        rim_light_sculpt = D.createGroupLayer(self._rim_light_name + " Sculpt")
        bounce_light_sculpt = D.createGroupLayer(self._bounce_light_name + " Sculpt")
        
        main_light_sculpt.setInheritAlpha(True)
        rim_light_sculpt.setInheritAlpha(True)
        bounce_light_sculpt.setInheritAlpha(True)

        main_light_sculpt.setBlendingMode('dodge')
        rim_light_sculpt.setBlendingMode('dodge')
        bounce_light_sculpt.setBlendingMode('dodge')
        
        # Create LS layers clones.
        main_light_clone = D.createCloneLayer(self._main_light_name + " Clone", self._main_light)
        rim_light_clone = D.createCloneLayer(self._rim_light_name + " Clone", self._rim_light)
        bounce_light_clone = D.createCloneLayer(self._bounce_light_name + " Clone", self._bounce_light)
        ambient_tint_clone = D.createCloneLayer(self._ambient_tint_name + " Clone", self._ambient_tint)
        ambient_lighten_clone = D.createCloneLayer(self._ambient_lighten_name + " Clone", self._ambient_lighten)
        ambient_darken_clone = D.createCloneLayer(self._ambient_darken_name + " Clone", self._ambient_darken)

        main_light_clone.setLocked(True)
        rim_light_clone.setLocked(True)
        bounce_light_clone.setLocked(True)
        ambient_tint_clone.setLocked(True)
        ambient_lighten_clone.setLocked(True)
        ambient_darken_clone.setLocked(True)

        ambient_tint_clone.setInheritAlpha(True)
        ambient_lighten_clone.setInheritAlpha(True)
        ambient_darken_clone.setInheritAlpha(True)

        ambient_tint_clone.setBlendingMode('hue')
        ambient_lighten_clone.setBlendingMode('screen')
        ambient_darken_clone.setBlendingMode('multiply')

        ambient_tint_clone.setOpacity(20)
        ambient_lighten_clone.setOpacity(63)
        ambient_darken_clone.setOpacity(63)
        
        # Create LS Sculpt groups Erase nodes
        main_light_erase_group = D.createNode(self._main_light_name + " Erase", 'grouplayer')
        rim_light_erase_group = D.createNode(self._rim_light_name + " Erase", 'grouplayer')
        bounce_light_erase_group = D.createNode(self._bounce_light_name + " Erase", 'grouplayer')

        main_light_erase_group.setBlendingMode("erase")
        rim_light_erase_group.setBlendingMode("erase")
        bounce_light_erase_group.setBlendingMode("erase")

        main_light_erase_0 = D.createNode("______", 'paintlayer')
        rim_light_erase_0 = D.createNode("______", 'paintlayer')
        bounce_light_erase_0 = D.createNode("______", 'paintlayer')

        main_light_erase_1 = D.createNode("Erase", 'paintlayer')
        rim_light_erase_1 = D.createNode("Erase", 'paintlayer')
        bounce_light_erase_1 = D.createNode("Erase", 'paintlayer')

        main_light_erase_1.setBlendingMode("erase")
        rim_light_erase_1.setBlendingMode("erase")
        bounce_light_erase_1.setBlendingMode("erase")

        main_light_erase_0.setPixelData(pixel_buffer_red, 0, 0, D.width(), D.height())
        rim_light_erase_0.setPixelData(pixel_buffer_red, 0, 0, D.width(), D.height())
        bounce_light_erase_0.setPixelData(pixel_buffer_red, 0, 0, D.width(), D.height())

        main_light_erase_group.addChildNode(main_light_erase_0, None)
        rim_light_erase_group.addChildNode(rim_light_erase_0, None)
        bounce_light_erase_group.addChildNode(bounce_light_erase_0, None)

        main_light_erase_group.addChildNode(main_light_erase_1, main_light_erase_group.childNodes()[-1])
        rim_light_erase_group.addChildNode(rim_light_erase_1, rim_light_erase_group.childNodes()[-1])
        bounce_light_erase_group.addChildNode(bounce_light_erase_1, bounce_light_erase_group.childNodes()[-1])

        # Finalize LS layers Sculpt groups.
        main_light_sculpt.addChildNode(main_light_clone, None)
        main_light_sculpt.addChildNode(main_light_erase_group, main_light_sculpt.childNodes()[-1])

        rim_light_sculpt.addChildNode(rim_light_clone, None)
        rim_light_sculpt.addChildNode(rim_light_erase_group, rim_light_sculpt.childNodes()[-1])

        bounce_light_sculpt.addChildNode(bounce_light_clone, None)
        bounce_light_sculpt.addChildNode(bounce_light_erase_group, bounce_light_sculpt.childNodes()[-1])
        
        # Create LS layers Sculpt groups Power clone.
        main_light_sculpt_power = D.createCloneLayer(main_light_sculpt.name() + " Power Clone", main_light_sculpt)
        rim_light_sculpt_power = D.createCloneLayer(rim_light_sculpt.name() + " Power Clone", rim_light_sculpt)
        bounce_light_sculpt_power = D.createCloneLayer(bounce_light_sculpt.name() + " Power Clone", bounce_light_sculpt)

        main_light_sculpt_power.setLocked(True)
        rim_light_sculpt_power.setLocked(True)
        bounce_light_sculpt_power.setLocked(True)

        main_light_sculpt_power.setInheritAlpha(True)
        rim_light_sculpt_power.setInheritAlpha(True)
        bounce_light_sculpt_power.setInheritAlpha(True)

        main_light_sculpt_power.setBlendingMode("dodge")
        rim_light_sculpt_power.setBlendingMode("dodge")
        bounce_light_sculpt_power.setBlendingMode("dodge")

        main_light_sculpt_power.setOpacity(127)
        rim_light_sculpt_power.setOpacity(127)
        bounce_light_sculpt_power.setOpacity(127)
        
        # Finalize LS Agent group.
        agent_group.addChildNode(ambient_tint_clone, None)
        agent_group.addChildNode(ambient_darken_clone, agent_group.childNodes()[-1])
        agent_group.addChildNode(ambient_lighten_clone, agent_group.childNodes()[-1])
        agent_group.addChildNode(bounce_light_sculpt, agent_group.childNodes()[-1])
        agent_group.addChildNode(bounce_light_sculpt_power, agent_group.childNodes()[-1])
        agent_group.addChildNode(rim_light_sculpt, agent_group.childNodes()[-1])
        agent_group.addChildNode(rim_light_sculpt_power, agent_group.childNodes()[-1])
        agent_group.addChildNode(main_light_sculpt, agent_group.childNodes()[-1])
        agent_group.addChildNode(main_light_sculpt_power, agent_group.childNodes()[-1])
        
        # Finalize final Group - LS_Shape
        if N.type() == 'grouplayer':
            N.setName("Shape")
            ls_shape.addChildNode(N.duplicate(), None)
        else:
            shape = D.createGroupLayer("Shape")
            shape.addChildNode(N.duplicate(), None)
            ls_shape.addChildNode(shape, None)

        ls_shape.addChildNode(agent_group, ls_shape.childNodes()[-1])

        # Finalize and cleanup
        parent.addChildNode(ls_shape, N)
        N.remove()
        D.refreshProjection()
    

    _ls_name: str = "Light System"
    
    _main_light_name = "Main Light"
    _rim_light_name = "Rim Light"
    _bounce_light_name = "Bounce Light"
    _ambient_tint_name = "Ambient Tint"
    _ambient_lighten_name = "Ambient Lighten"
    _ambient_darken_name = "Ambient Darken"
    _ambient_name = "Ambient"
    
    _light_system = None
    
    _main_light = None
    _rim_light = None
    _bounce_light = None
    _ambient_tint = None
    _ambient_lighten = None
    _ambient_darken = None




#print(N.pixelData(0, 0, D.width(), D.height()))
'''
print(D.pixelData(0, 0, 10, 10).toHex("_"))
print(D.pixelData(0, 0, 1, 1))
q_byte_array = QByteArray()
print(q_byte_array.fromHex(b'000000ff'))

for x in range(0, 40, 4):
    print(x)
    q_byte_array.append(QByteArray.fromHex(b'000000ff'))
print(q_byte_array.toHex())
'''
#print(D.backgroundColor().red())


ls = LightSystem()
ls.setup_ls_agent()