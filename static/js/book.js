document.addEventListener("DOMContentLoaded", function() {
    const packageSelect = document.getElementById('package');
    const optionsContainer = document.getElementById('options-container');

    packageSelect.addEventListener('change', function() {
        const packageId = this.value;
        if (packageId) {
            fetch(`/get_package_options/${packageId}`)
            .then(response => response.json())
            .then(data => {
                // Clear previous options
                optionsContainer.innerHTML = '';

                // Add new options based on package selection
                // Example: venues (radio buttons), themes (radio buttons), games (checkboxes), etc.
                // You can customize this based on your Package model structure
                for (const [optionName, options] of Object.entries(data)) {
                    const optionLabel = document.createElement('label');
                    optionLabel.textContent = optionName + ':';
                    optionsContainer.appendChild(optionLabel);
                    optionsContainer.appendChild(document.createElement('br'));
                    
                    for (const option of options) {
                        const input = document.createElement('input');
                        input.type = (optionName === 'venues' || optionName === 'themes') ? 'radio' : 'checkbox';
                        input.name = optionName;
                        input.value = option;
                        const label = document.createElement('label');
                        label.textContent = option;
                        optionsContainer.appendChild(input);
                        optionsContainer.appendChild(label);
                        optionsContainer.appendChild(document.createElement('br'));
                    }
                }
                optionsContainer.style.display = 'block';
            });
        } else {
            optionsContainer.innerHTML = '';
            optionsContainer.style.display = 'none';
        }
    });
});