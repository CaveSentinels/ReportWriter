jQuery(function() {

    // handle form readonly layout
    $(".readonly input, .readonly textarea, .readonly select").prop('disabled', true);
    $(".readonly button").hide();
    $(".readonly #id_selected_cwes").css("width", "100%");

    var cwe_select = $("#id_selected_cwes");
    var page_limit = cwe_select.data('page-limit');

    // Make CWE selection a multiple ajax select2
    cwe_select.select2({
        placeholder: "Either click 'Suggest CWEs' to get the suggest CWE based on your description or select a CWE from the list",
        ajax: {
            url: $(this).data('ajax-url'),
            dataType: 'json',
            delay: 250,
            data: function (params) {
              return {
                  q: params.term, // search term
                  page: params.page
              };
            },

            processResults: function (data, params) {
              // parse the results into the format expected by Select2.
              // since we are using custom formatting functions we do not need to
              // alter the remote JSON data
                params.page = params.page || 1;
                return {
                    results: data.items,
                    pagination: {
                        more: (params.page * page_limit) < data.total_count
                    },
                };
            },
            cache: true
        },

        minimumInputLength: 0,
    });

    // populate CWEs with initial data
    if (cwe_select.data('report-id')) {
        var $request = $.ajax({url: cwe_select.data('init-url'), data: {'report_id': cwe_select.data('report-id')} });
        $request.then(function (data) {

            var cwes = data.items
            for (var i = 0; i < cwes.length; i++) {
                var item = cwes[i];
                var option = new Option(item.text, item.id, true, true);

                cwe_select.append(option);
            }

            cwe_select.trigger('change');

            // a switch to indicate the CWE selection has changed so we do appropriate actions in the views
            // the switch is added here because we want to listedn for changes after initializing the data
            cwe_select.change(function() {
                $('#cwe_changed').val(true);
            });
        });
    } else {
        // a switch to indicate the CWE selection has changed so we do appropriate actions in the views
        cwe_select.change(function() {
            $('#cwe_changed').val(true);
        });
    }


    // get CWE suggestions
    $("body").on('click', '#cwe-suggestion-button', function(e){
        var description = $('#id_description').val();
        if (description) {
            // Description is present, we need to make a call to the Enhanced CWE application to get the related CWEs
            $.ajax({
                url: $(this).data('ajax-url'),
                data: {description: description},

                success: function (result) {
                    cwe_select.empty()
                    $.each(result.items, function() {
                        var option = new Option(this.text, this.id, true, true);
                        cwe_select.append(option)
                    });
                    cwe_select.trigger("change");
                },

                error: function (xhr, errmsg, err) {
                    alert("Oops! We have encountered and error \n" + errmsg);
                }
            });
        }
    });

    // Make MUO fields not readonly before submitting the form or else the values won't be submitted
    $("#report_form").submit(function( event ) {
        // Only if the whole form is not intended to be readonly
        if (!$('#report-container').hasClass('readonly')) {
            var muo_container = $('#custom-muo-container');
            muo_container.find('input:disabled, textarea:disabled, select:disabled').prop('disabled', false);
        }
    });


    $("body").on('click', '#misusecase-suggestion', function(e){
        // Show the muo selection container with pre-populated misuse case related to the cwes. Also hide the custom
        // MUO creation form
        e.preventDefault();

        // If there is some already selected misuse case, don't reload the misuse cases again
        var last_selected_misuse_case_id = $('.misuse-case-container.selected').attr("data-value");
        if (last_selected_misuse_case_id == undefined) {
            var cwe_code_string = '';
            var delimiter = '';

            // Get all the CWEs selected and loop over it. Value of each selected option is in the format
            // 'CWE Code'_'CWE Name'. We need to get a string of all the selected CWE codes in comma separated format
            cwe_select.val().forEach(function(item) {
                // Append the delimiter value to the CWE code string
                cwe_code_string = cwe_code_string.concat(delimiter);

                // Split the value on hyphen(-), and get the first element of the array, which is CWE code
                var code = item.split('_')[0];

                // Concatenate the code in the string of CWE codes
                cwe_code_string = cwe_code_string.concat(code);

                // Change the delimiter value to ','
                delimiter = ',';
            });

            // Load the misuse cases for the selected CWEs
            load_misusecases(cwe_code_string);
        }

        $('#custom-muo-container').hide();
        $('#muo-container').show();
    });

    $("body").on('click', '#misusecase-custom', function(e){
        // Show the muo creation div. Also hide the muo selection container
        e.preventDefault();
        $('#muo-container').hide();
        $('#custom-muo-container').show();

        // Make the is_custom_muo boolean variable true
        toggl_is_custom_muo(true);
    });

    $("body").on('click', '#muo-close', function(e){
        // Hide the muo selection container
        e.preventDefault();
        $('#muo-container').hide();
    });

    $("body").on('click', '#muo-select', function(e){
        e.preventDefault();

        // Get the selected misuse case and use case divs
        var selected_misuse_case_div = $('.misuse-case-container.selected');
        var selected_use_case_div = $('.use-case-container.selected');

        if (selected_misuse_case_div.attr("data-value") == undefined &&
            selected_use_case_div.attr("data-value") == undefined) {
            // No misuse case and use case is selected
            alert('You must select at least a misuse case or close the suggested ones and write your own misuse ' +
                  'case and use case')

        }
        else if (selected_misuse_case_div.attr("data-value") != undefined &&
                 selected_use_case_div.attr("data-value") == undefined) {
            // Misuse case is selected but no use case is selected
            var myAlert = confirm('You have only selected a misuse case. Are you sure you want to write your own use case?' +
                                  '\nClick \'OK\' to continue or \'Cancel\' to select the use case');
            if (myAlert == true) {
                // If user clicked ok, hide the MUO selection div and show the custom MUO creation div. Also populate
                // the fields of custom MUO creation div with the selection
                $('#muo-container').hide();
                $('#custom-muo-container').show();
                populate_muo_fields();

                // Make the is_custom_muo boolean variable true
                toggl_is_custom_muo(true);
            }
        }
        else {
            // Misuse case and use case is selected

            // Populate the
            populate_muo_fields();

            // Hide the muo selection container and show the muo creation div with all the fields disabled
            $('#muo-container').hide();
            $('#custom-muo-container').show();

            // Make the is_custom_muo boolean variable true
            toggl_is_custom_muo(false);
        }
    });

    $("body").on('click', '.misuse-case-container', function(){
        // get the misuse case id of the clicked misuse case
        var misuse_case_id = $(this).attr("data-value");

        // get the misuse case id of the last selected misuse case
        var last_selected_misuse_case_id = $('.misuse-case-container.selected').attr("data-value");

        // If the selected misuse case is clicked again, do nothing, otherwise send the ajax
        // request to get the use cases corresponding to the clicked misuse case
        if (misuse_case_id != last_selected_misuse_case_id) {
            // Remove the selection from the last selected misuse case div
            $('.misuse-case-container.selected').removeClass('selected');

            // Select the current div
            $(this).addClass('selected');

            // Load usecases corresponding to the selected misuse
            load_usecases(misuse_case_id);
        }
    });

    $("body").on('click', '.use-case-container', function(){
        // get the use case id of the clicked misuse case
        var use_case_id = $(this).attr("data-value");

        // get the use case id of the last selected use case
        var last_selected_use_case_id = $('.use-case-container.selected').attr("data-value");

        // If the selected use case is clicked again, do nothing, otherwise add the css to the currently
        // selected use case
        if (use_case_id != last_selected_use_case_id) {
            // Remove the selection from the last selected misuse case div
            $('.use-case-container.selected').removeClass('selected');

            // Select the current div
            $(this).addClass('selected');
        }
    });

    $("input[name='osr-pattern']").change(function(){
        // Set the placeholder based on the selection
        var value = $(this).val();
        set_placeholder(value);
    });
});


function load_misusecases(cwe_codes_string) {
    $.ajax({
        url: 'report_report_misusecases/',
        type: 'POST',
        data: {cwe_codes: cwe_codes_string}, // Send the selected CWE codes

        success: function(result) {
            $('.slim-scroll-div').replaceWith(result);
        },

        error: function (xhr,errmsg,err) {
            alert("Oops! We have encountered and error \n" + errmsg);
        }
    });
}


function load_usecases(misuse_case_id) {
    $.ajax({
        url: 'report_report_usecases/',
        type: 'POST',
        data: {misuse_case_id: misuse_case_id}, // Send the selected misuse case id

        success: function(result) {
            // If ajax call is successful, reload the fat-scroll-div which contains the use cases
            $('.fat-scroll-div').replaceWith(result);
        },

        error: function(xhr,errmsg,err) {
            // Show error message in the alert
            alert("Oops! We have encountered and error \n" + errmsg);
        }
    });
}


function set_placeholder(value) {
    var placeholder = 'Please write the requirements in the following format:\n';
    var addendum;
    switch(parseInt(value)) {
        case 1:
            addendum = "The <system name> shall <system response>\n\n" +
                                "Example: The software shall be written in Java";
            break;
        case 2:
            addendum = "WHEN <trigger> <optional precondition> the <system name> shall <system respons>\n\n" +
                                "Example: When a DVD is inserted into the DVD player, the OS shall spin up the optical drive";
            break;
        case 3:
            addendum = "IF <unwanted condition or event>, THEN the <system name> shall <system response>\n\n" +
                                "Example: If the memory checksum is invalid, then the software shall display an error message";
            break;
        case 4:
            addendum = "WHILE <system state>, the <system name> shall <system response>\n\n" +
                                "Example: While the heater is on, the software shall close the water intake valve";
            break;
        default:
            addendum = '';
    }
    placeholder = placeholder.concat(addendum);

    // Set the placeholder of the OSR text area
    $('#osr-description').attr("placeholder", placeholder);
}


function populate_muo_fields() {
    var selected_misuse_case_div = $('.misuse-case-container.selected');
    var selected_use_case_div = $('.use-case-container.selected');

    $('#id_misuse_case_description').val(selected_misuse_case_div.find('.misuse-case-div').text().trim());
    $('#id_use_case_description').val(selected_use_case_div.find('.use-case-div').text().trim());
    $('#id_osr').val(selected_use_case_div.find('.osr-div').text().trim());
}

function toggl_is_custom_muo(is_muo_custom) {
    // Change the value of the hidden field
    $("#custom-muo-flag").attr("value", is_muo_custom);
    $('#custom-muo-container textarea').attr('disabled', !is_muo_custom);
}