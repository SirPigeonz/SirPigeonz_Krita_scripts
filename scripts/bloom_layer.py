from krita import *

K = Krita.instance()
D = K.activeDocument()
N = D.activeNode()


def create_bloom_layer():
    parent = N.parentNode()
    
    if D.selection() == None:
        K.action("select_all").trigger()
        D.tryBarrierLock()
        D.waitForDone()
        selection = D.selection()
        D.unlock()
        selection = D.selection()
        #print("selection is: " + str(selection))
        K.action("deselect").trigger()
    else:
        selection = D.selection()
    
    
    curves = K.filter("perchannel")
    bloom_layer = D.createFilterLayer("Bloom Layer", curves, selection)
    blur = K.filter("blur")
    blur_mask = D.createFilterMask("Blur", blur, selection)
    #transparency_mask = D.createNode("Transparency", "transparencymask")
    #s = selection
    #transparency_mask.setPixelData(selection.pixelData(s.x(), s.y(), s.width(), s.height()), s.x(), s.y(), s.width(), s.height())
    #print(transparency_mask.channels())
    #bloom_layer.addChildNode(transparency_mask, None)
    bloom_layer.addChildNode(blur_mask, None)
    bloom_layer.setBlendingMode("screen")
    parent.addChildNode(bloom_layer, N)
    
    
    '''
    #group = D.createGroupLayer("Bloom")
    clone = D.createCloneLayer("Bloom", N)
    print(K.filters())
    curve_filter = K.filter("perchannel")
    curve_fmask = D.createFilterMask("Curve Filter", curve_filter, selection)

    #parent.addChildNode(group, N)
    #group.addChildNode(clone, None)
    clone.addChildNode(curve_fmask, None)
    parent.addChildNode(clone, N)
    '''
    

create_bloom_layer()

