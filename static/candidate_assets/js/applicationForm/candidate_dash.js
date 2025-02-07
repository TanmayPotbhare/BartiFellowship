const researchPaperSelect = document.getElementById('research_paper_select');
const researchPaperUpload = document.getElementById('research_paper_upload');
const feedback_select = document.getElementById('feedback_select');
const write_feedback = document.getElementById('write_feedback');
const research_paper_file = document.getElementById('research_paper_file');
const write_feedback_here = document.getElementById('write_feedback_here');

researchPaperSelect.addEventListener('change', function() {
    if (this.value === 'Yes') {
        researchPaperUpload.style.display = 'block';
    } else {
        researchPaperUpload.style.display = 'none';
        research_paper_file.value = '';
    }
});

feedback_select.addEventListener('change', function() {
    if (this.value === 'Yes') {
        write_feedback.style.display = 'block';
    } else {
        write_feedback.style.display = 'none';
        write_feedback_here.value = '';
    }
});