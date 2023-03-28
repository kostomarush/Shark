/*
Template Name: Greeva - Responsive Bootstrap 4 Admin Dashboard
Author: CoderThemes
Version: 2.0.0
Website: https://coderthemes.com/
Contact: support@coderthemes.com
File: Form advanced init js
*/

!function($) {
    "use strict";

    var FormAdvanced = function() {};

    //Select2
    FormAdvanced.prototype.initSelect2 = function() {
        // Select2
        $('[data-toggle="select2"]').select2();
    },

    
    //initializing Switchery
    FormAdvanced.prototype.initSwitchery = function() {
        $('[data-plugin="switchery"]').each(function (idx, obj) {
            new Switchery($(this)[0], $(this).data());
        });
    },

    //Max Length
    FormAdvanced.prototype.initMaxLength = function() {
        //Bootstrap-MaxLength
        $('input#defaultconfig').maxlength({
            warningClass: "badge badge-success",
            limitReachedClass: "badge badge-danger"
        });

        $('input#thresholdconfig').maxlength({
            threshold: 20,
            warningClass: "badge badge-success",
            limitReachedClass: "badge badge-danger"
        });

        $('input#alloptions').maxlength({
            alwaysShow: true,
            separator: ' out of ',
            preText: 'You typed ',
            postText: ' chars available.',
            validate: true,
            warningClass: "badge badge-success",
            limitReachedClass: "badge badge-danger"
        });

        $('textarea#textarea').maxlength({
            alwaysShow: true,
            warningClass: "badge badge-success",
            limitReachedClass: "badge badge-danger"
        });

        $('input#placement').maxlength({
            alwaysShow: true,
            placement: 'top-left',
            warningClass: "badge badge-success",
            limitReachedClass: "badge badge-danger"
        });
    },

    //Time Picker
    FormAdvanced.prototype.initTimePicker = function() {
        $('#timepicker').timepicker({
            defaultTIme: false,
            icons: {
                up: 'mdi mdi-chevron-up',
                down: 'mdi mdi-chevron-down'
            }
        });
        $('#timepicker2').timepicker({
            showMeridian: false,
            icons: {
                up: 'mdi mdi-chevron-up',
                down: 'mdi mdi-chevron-down'
            }
        });
        $('#timepicker3').timepicker({
            minuteStep: 10,
            icons: {
                up: 'mdi mdi-chevron-up',
                down: 'mdi mdi-chevron-down'
            }
        });
    },

    // colorpicker
    FormAdvanced.prototype.initColorPicker = function() {
        $('.colorpicker-default').colorpicker({
            format: 'hex'
        });
        $('.colorpicker-rgba').colorpicker();
    },

    // colorpicker
    FormAdvanced.prototype.initInputMask = function() {
        $('[data-toggle="input-mask"]').each(function (idx, obj) {
            var maskFormat = $(obj).data("maskFormat");
            var reverse = $(obj).data("reverse");
            if (reverse != null)
                $(obj).mask(maskFormat, {'reverse': reverse});
            else
                $(obj).mask(maskFormat);
        });
    },

    // colorpicker
    FormAdvanced.prototype.initDateRangePicker = function() {
        $('.input-daterange-datepicker').daterangepicker({
            buttonClasses: ['btn', 'btn-sm'],
            applyClass: 'btn-success',
            cancelClass: 'btn-light'
        });
        $('.input-daterange-timepicker').daterangepicker({
            timePicker: true,
            timePickerIncrement: 30,
            locale: {
                format: 'MM/DD/YYYY h:mm A'
            },
            buttonClasses: ['btn', 'btn-sm'],
            applyClass: 'btn-success',
            cancelClass: 'btn-light'
        });
        $('.input-limit-datepicker').daterangepicker({
            format: 'MM/DD/YYYY',
            minDate: '06/01/2018',
            maxDate: '06/30/2018',
            buttonClasses: ['btn', 'btn-sm'],
            applyClass: 'btn-success',
            cancelClass: 'btn-light',
            dateLimit: {
                days: 6
            }
        });

        $('#reportrange span').html(moment().subtract(29, 'days').format('MMMM D, YYYY') + ' - ' + moment().format('MMMM D, YYYY'));

        $('#reportrange').daterangepicker({
            format: 'MM/DD/YYYY',
            startDate: moment().subtract(29, 'days'),
            endDate: moment(),
            minDate: '01/01/2017',
            maxDate: '12/31/2020',
            dateLimit: {
                days: 60
            },
            showDropdowns: true,
            showWeekNumbers: false,
            timePicker: false,
            timePickerIncrement: 1,
            timePicker12Hour: true,
            ranges: {
                'Today': [moment(), moment()],
                'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
                'Last 7 Days': [moment().subtract(6, 'days'), moment()],
                'Last 30 Days': [moment().subtract(29, 'days'), moment()],
                'This Month': [moment().startOf('month'), moment().endOf('month')],
                'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
            },
            opens: 'left',
            drops: 'down',
            buttonClasses: ['btn', 'btn-sm'],
            applyClass: 'btn-success',
            cancelClass: 'btn-light',
            separator: ' to ',
            locale: {
                applyLabel: 'Submit',
                cancelLabel: 'Cancel',
                fromLabel: 'From',
                toLabel: 'To',
                customRangeLabel: 'Custom',
                daysOfWeek: ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'],
                monthNames: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
                firstDay: 1
            }
        }, function (start, end, label) {
            console.log(start.toISOString(), end.toISOString(), label);
            $('#reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
        });
    },

    //initilizing
    FormAdvanced.prototype.init = function() {
        var $this = this;
        this.initSelect2();
        this.initSwitchery();
        this.initMaxLength();
        this.initTimePicker();
        this.initColorPicker();
        this.initInputMask();
        this.initDateRangePicker();

    },

    $.FormAdvanced = new FormAdvanced, $.FormAdvanced.Constructor = FormAdvanced

}(window.jQuery),
    //initializing main application module
    function ($) {
        "use strict";
        $.FormAdvanced.init();
    }(window.jQuery);