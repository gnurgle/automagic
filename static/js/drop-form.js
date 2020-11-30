let year_select = document.getElementById('year');
let make_select = document.getElementById('make');
let model_select = document.getElementById('model');
let trim_select = document.getElementById('trim');
let partCat_select = document.getElementById('partCat');
let partList_select = document.getElementById('partList');



        year_select.onchange = function() {
            year = year_select.value;
            fetch('/' + year + '/make/model/trim').then(function(response) {
                response.json().then(function(data) {
                    optionHTML = ''
                    for (let make of data.makes){
                        optionHTML += '<option value="' + make + '">' + make + '</option>';
                    }
                    make_select.innerHTML = optionHTML;

                    optionHTML = ''
                    for (let model of data.models){
                        optionHTML += '<option value="' + model + '">' + model + '</option>';
                    }
                    model_select.innerHTML = optionHTML;

                    optionHTML = ''
                    for (let trim of data.trims){
                        optionHTML += '<option value="' + trim + '">' + trim + '</option>';
                    }
                    trim_select.innerHTML = optionHTML;
                })
            });
        }

        make_select.onchange = function() {
            year = year_select.value;
            make = make_select.value;
            fetch('/' + year + '/'+ make +'/model/trim').then(function(response) {
                response.json().then(function(data) {
                    optionHTML = ''
                    for (let model of data.models){
                        optionHTML += '<option value="' + model + '">' + model + '</option>';
                    }
                    model_select.innerHTML = optionHTML;

                    optionHTML = ''
                    for (let trim of data.trims){
                        optionHTML += '<option value="' + trim + '">' + trim + '</option>';
                    }
                    trim_select.innerHTML = optionHTML;
                })
            });
        }
        model_select.onchange = function() {
            year = year_select.value;
            make = make_select.value;
            model = model_select.value;

            fetch('/' + year + '/'+ make +'/'+ model +'/trim').then(function(response) {
                response.json().then(function(data) {
                    optionHTML = ''
                    for (let trim of data.trims){
                        optionHTML += '<option value="' + trim + '">' + trim + '</option>';
                    }
                    trim_select.innerHTML = optionHTML;
                })
            });
        }

        partCat_select.onchange = function() {
            var year = document.getElementById("year").getAttribute("data-value");
            var make = document.getElementById("make").getAttribute("data-value");
            var model = document.getElementById("model").getAttribute("data-value");
            var trim = document.getElementById("trim").getAttribute("data-value");
			
            partType = partCat_select.value;
            fetch('/' + year + '/' + make + '/' + model + '/' + trim + '/' + partType + '/partList').then(function(response) {
                response.json().then(function(data) {
                    optionHTML = ''
                    for (let partList of data.partList){
                        optionHTML += '<option value="' + partList + '">' + partList + '</option>';
                    }
                    partList_select.innerHTML = optionHTML;
                })
            });
        }
