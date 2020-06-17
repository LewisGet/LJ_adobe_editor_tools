/* 1) Create an instance of CSInterface. */
var cs_interface = new CSInterface();

/* 2) Make a reference to your HTML button and add a click handler. */
var open_button = document.querySelector("#open-button");
open_button.addEventListener("click", open_doc);

/* 3) Write a helper function to pass instructions to the ExtendScript side. */
function open_doc() {
  cs_interface.evalScript("open_document()");
}
