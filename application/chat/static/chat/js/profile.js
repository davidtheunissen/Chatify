document.addEventListener('DOMContentLoaded', function() {

    // Disable default link behavior
    document.querySelectorAll('.profile-link').forEach(function(link) {
        link.style.textDecoration = 'none';
    });
    
    // Hover over background color change
    document.querySelectorAll('li').forEach(function(li) {
        li.onmouseover = function() {
            li.classList.add('bg-light');
        };
        li.onmouseout = function() {
            li.classList.remove('bg-light');
        };
    });

});