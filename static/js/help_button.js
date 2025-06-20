/* if a question mark is clicked, display the help text associated 
   with the nearest specialty button */
document.querySelectorAll('.question-mark').forEach(function(question) {
 question.addEventListener('click', function(event) {
  event.stopPropagation(); 
  let wrapper = question.closest('.button-help-wrapper');
  wrapper.classList.toggle('show-help');
 });
});

// hide help text once clicked off of 
document.addEventListener('click', function() {
 document.querySelectorAll('.button-help-wrapper').forEach(function(wrapper) {
  wrapper.classList.remove('show-help');
 });
});
