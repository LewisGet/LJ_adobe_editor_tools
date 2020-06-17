var cs_interface = new CSInterface();

var clone_lewis = document.querySelector("#clone-lewis");

clone_lewis.addEventListener("click", function(){
    cs_interface.evalScript("clone_lewis()");
});

var clone_kevin = document.querySelector("#clone-kevin");

clone_kevin.addEventListener("click", function(){
    cs_interface.evalScript("clone_kevin()");
});

var clone_gold = document.querySelector("#clone-gold");

clone_gold.addEventListener("click", function(){
    cs_interface.evalScript("clone_gold()");
});
