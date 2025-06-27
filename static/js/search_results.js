let currentPage = 1;
let updateRowClickHandlers, updatePaginationLinks, updatePaginationSpan, fetchPage;
const exportLink = document.getElementById('export-csv');
const grantCheckbox = document.getElementById('show_trials');

/* listen for changes to sorting criteria once results are loaded */
$(document).ready(function() {
 $('#order_criteria, #order_asc').change(function(event) {
  event.preventDefault();
  let criteria = $('#order_criteria').val();
  let ascend = $('#order_asc').val();
  sortResults(criteria, ascend);
 });
});

/* listen for checking/unchecking of trials box; on change, 
   jump back to page 1 */
grantCheckbox.addEventListener('change', () => {
 fetchPage(1, $('#order_criteria').val(), $('#order_asc').val());
});


 /* dynamically sort without reloading */
function sortResults(criteria, ascend) {
 const showTrials = grantCheckbox.checked;
 $.ajax({
  url: `search/page/${currentPage}`
     + `?sort_criteria=${criteria}`
     + `&ascend=${ascend}`
     + `&show_trials=${showTrials}`,
  method: 'GET',
  success: function(data) {
   $('#results tbody').html($(data).find('#results tbody').html());
   $('#total_pages').val($(data).find('#total_pages').val());
   updateRowClickHandlers();
   updatePaginationLinks();
   updatePaginationSpan();
  }
 });
}

document.addEventListener('DOMContentLoaded', function() {
 const rows = document.querySelectorAll('#results tbody tr');
 const perPage = 25;

 /* pagination of results */
 fetchPage = function(page, criteria='similarity', ascend='DESC') {
  const showTrials = grantCheckbox.checked;
  $.ajax({ 
   url: `/search/page/${page}?`
      + `sort_criteria=${criteria}`
      + `&ascend=${ascend}`
      + `&show_trials=${showTrials}`,
   method: 'GET',
   success: function(data) {
    $('#results tbody').html($(data).find('#results tbody').html());
    $('#total_pages').val($(data).find('#total_pages').val());
    currentPage = page;
    updateRowClickHandlers();
    updatePaginationLinks();
    updatePaginationSpan();
   }
  });
 }

 /* expands/retracts row upon click for full/preview description */
 updateRowClickHandlers = function() {
  const rows = document.querySelectorAll('#results tbody tr');
  rows.forEach(row  => {
   row.addEventListener('click', function() {
    const descriptionCell = this.querySelector('.brief-description');
    
    if (descriptionCell.classList.contains('expanded')) {
     descriptionCell.classList.remove('expanded');
     descriptionCell.textContent = descriptionCell.textContent.slice(0, 100);
     descriptionCell.textContent += '...';
    } else {
     descriptionCell.classList.add('expanded');
     descriptionCell.textContent = this.dataset.fullDescription;
    }
   });
  });
 }

 /* paginated results - buttons and navigation */
 updatePaginationLinks = function() {
  const prevLink = document.querySelector('.pagination .prev');
  const nextLink = document.querySelector('.pagination .next');
  const totalPages = parseInt(document.getElementById('total_pages').value);
  
  if (prevLink) {
   prevLink.replaceWith(prevLink.cloneNode(true));
  }
  if (nextLink) {
   nextLink.replaceWith(nextLink.cloneNode(true));
  }

  const newPrev = document.querySelector('.pagination .prev');
  const newNext = document.querySelector('.pagination .next');
  if (newPrev) {
   newPrev.addEventListener('click', function(event) {
    event.preventDefault();
    const page = currentPage - 1;
    
    if (page > 0) {
     let criteria = $('#order_criteria').val();
     let ascend = $('#order_asc').val();
     fetchPage(page, criteria, ascend);
    } 
   });
  }
  
  if (newNext) {
   newNext.addEventListener('click', function(event) {
    event.preventDefault(); 
    const page = currentPage + 1;
    
    if (page <= totalPages) {
     let criteria = $('#order_criteria').val();
     let ascend = $('#order_asc').val();
     fetchPage(page, criteria, ascend);
    }

    if (!prevLink && currentPage > 1) {
     const newElem = document.createElement('a');
     const target = document.getElementById('pagination');

     newElem.setAttribute('href', '#');
     newElem.setAttribute('class', 'prev');
     newElem.innerHTML = '&laquo; Previous';

     target.appendChild(newElem);
    }
   });
  }
 }

 updatePaginationSpan = function() {
  const spanElement = document.querySelector('.page-numbers');
  const totalPages = parseInt(document.getElementById('total_pages').value);
  spanElement.textContent = `Page ${currentPage} of ${totalPages}`;
 }

 fetchPage(currentPage);
});