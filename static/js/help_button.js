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

// search specialty query once button clicked
document.querySelectorAll('.main-button').forEach(button => {
 button.addEventListener('click', e => {
  const query = encodeURIComponent(e.currentTarget.dataset.query);
  const display = encodeURIComponent(e.currentTarget.dataset.display);
  window.location.href = `/search?query=${query}&display=${display}`;
 });
});