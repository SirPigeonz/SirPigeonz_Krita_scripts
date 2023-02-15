from krita import *

K = Krita.instance()
D = K.activeDocument()
N = D.activeNode()


def create_bloom_layer(gauss_blur: bool = True):
    #print(K.filters())
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
    
    n_name = ""
    blur = None
    if gauss_blur:
        blur = K.filter("gaussian blur")
        n_name = "Gaussian Blur"
    else:
        blur = K.filter("blur")
        n_name = "Simple Blur"
    
    blur_mask = D.createFilterMask(n_name, blur, selection)
    bloom_layer.addChildNode(blur_mask, None)
    bloom_layer.setBlendingMode("screen")
    parent.addChildNode(bloom_layer, N)


create_bloom_layer(True)

