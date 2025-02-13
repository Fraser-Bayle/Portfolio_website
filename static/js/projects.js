$(document).ready(function() {
    const projectGrid = $('.project-grid');
    const filterForm = $('#tag-filter-form');

    function loadProjects(selectedTags = []) {
        let url = '/api/projects/';
        if (selectedTags.length > 0) {
            url += '?tags=' + selectedTags.join(',');
        }

        $.ajax({
            url: url,
            method: 'GET',
            success: function(data) {
                projectGrid.empty();

                if (data.length === 0) {
                    projectGrid.append('<p class="pixel-text">No projects found matching the selected tags.</p>');
                    return;
                }

                data.forEach(project => {
                    const projectCard = `
                        <a href="/projects/${project.id}/" class="project-link">
                            <div class="project-card pixel-border">
                                ${project.thumbnail 
                                    ? `<img src="${project.thumbnail}" alt="${project.title} thumbnail" class="project-thumbnail">`
                                    : `<div class="project-thumbnail placeholder pixel-text">No Image</div>`
                                }
                                <h2 class="project-title pixel-text">${project.title}</h2>
                                <p class="project-description">${project.description.split(' ').slice(0, 20).join(' ')}...</p>
                                <div class="project-tags">
                                    <span class="pixel-text">Tags:</span>
                                    ${project.tags.map(tag => `
                                        <span class="tag">${tag.name}</span>
                                    `).join(', ')}
                                </div>
                            </div>
                        </a>
                    `;
                    projectGrid.append(projectCard);
                });
            },
            error: function(xhr, status, error) {
                console.error('Error fetching projects:', error);
                projectGrid.html('<p class="pixel-text">Error loading projects. Please try again later.</p>');
            }
        });
    }

    filterForm.on('submit', function(e) {
        e.preventDefault();
        const selectedTags = [];
        $('input[name="tags"]:checked').each(function() {
            selectedTags.push($(this).val());
        });
        loadProjects(selectedTags);
    });

    // Load all projects on initial page load
    loadProjects();
});