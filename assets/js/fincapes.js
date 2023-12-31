/*
 ** FINCAPES Project
 */
;
(function ($) {
    'use strict';

    $.FincapesCore = {
        init: function () {
            $(document).ready(function (e) {
                if ($('[data-bg-img-src]').length) $.FincapesCore.helpers.bgImage($('[data-bg-img-src]'));
                if ($("[data-img-src]").length) $.FincapesCore.helpers.imageSrc($('[data-img-src]'));
                $.FincapesCore.helpers.extendjQuery();
            });

            $(window).on('load', function (e) {

            });
        },

        components: {},

        helpers: {
            bgImage: function (collection) {

                if (!collection || !collection.length) return;

                return collection.each(function (i, el) {

                    var $el = $(el),
                        bgImageSrc = $el.data('bg-img-src');

                    if (bgImageSrc) $el.css('background-image', 'url(' + bgImageSrc + ')');
                });
            },
            imageSrc: function (collection) {
                if (!collection || !collection.length) return;
                return collection.each(function (i, el) {
                    var $el = $(el),
                        imgSrc = $el.data('img-src');
                    if (imgSrc) $el.attr('src', imgSrc);
                })
            },
            bsUpdate: function (collection) {
                if (!collection || !collection.length) return;
                var config = {
                    formURL: null,
                    asyncUpdate: false,
                    modalID: '#modal',
                    errorClass: '.is-invalid',
                    isDeleteForm: false,
                    asyncSettings: {
                        closeOnSubmit: true,
                        successMessage: null,
                        dataUrl: null,
                        dataElementId: null,
                        dataKey: "response",
                        addModalFormFunction: null
                    }
                }
                return collection.each(function (i, el) {
                    let $el = $(el),
                        successMsg = [
                            "<script>$('#save-me').show().delay(1000).fadeOut();</script>"
                        ].join();

                    function updateModal() {
                        $el.each(function () {
                            $(this).modalForm({
                                formURL: $(this).data('form-url'),
                                errorClass: config.errorClass,
                                modalID: $(this).data('modal-id') ? $(this).data('modal-id') : config.modalID,
                                asyncUpdate: $(this).data('async-update') ? $(this).data('async-update') : config.asyncUpdate,
                                isDeleteForm: $(this).data('is-delete') ? $(this).data('is-delete') : config.isDeleteForm,
                                asyncSettings: {
                                    closeOnSubmit: $(this).data('close-on-submit') ? $(this).data('close-on-submit') : config.asyncSettings.closeOnSubmit,
                                    successMessage: successMsg,
                                    dataUrl: $(this).data('response-url') ? $(this).data('response-url') : config.asyncSettings.dataUrl,
                                    dataElementId: $(this).data('element-id') ? $(this).data('element-id') : config.asyncSettings.dataElementId,
                                    dataKey: $(this).data('key') ? $(this).data('key') : config.asyncSettings.dataKey,
                                    addModalFormFunction: updateModal
                                }
                            })
                        })
                    }
                    updateModal()
                })
            },

            extendjQuery: function () {
                $.fn.extend({
                    imagesLoaded: function () {

                        var $imgs = this.find('img[src!=""]');

                        if (!$imgs.length) {
                            return $.Deferred().resolve().promise();
                        }

                        var dfds = [];

                        $imgs.each(function () {
                            var dfd = $.Deferred();
                            dfds.push(dfd);
                            var img = new Image();
                            img.onload = function () {
                                dfd.resolve();
                            };
                            img.onerror = function () {
                                dfd.resolve();
                            };
                            img.src = this.src;
                        });

                        return $.when.apply($, dfds);
                    }
                });
            }
        }
    };

    $.FincapesCore.components.dataTable = {
        pageCollection: $(),
        init: function (selector) {
            this.collection = selector && $(selector).length ? $(selector) : $();
            if (!$(selector).length) return;
            this.initDataTable();
            return this.pageCollection
        },

        initDataTable: function () {
            this.collection.each(function (i, el) {
                let $this = $(el),
                    customDom;
                if ($this.attr('data-custom-dom')) {
                    customDom = "<'row mb-3 d-flex align-items-baseline'<'col-lg-9 col-sm-6'" +
                            "<'#toolbar'>><'col-lg-3 col-sm-6'>><'row'<'col-sm-12'tr>>" +
                            "<'row'<'col-sm-5'i><'col-sm-7'p>>"
                } else {
                    customDom = "<'row mb-3'<'col-lg-10 col-sm-7'><'col-lg-2 col-sm-5 text-end'<'#btn-actions'>>>" +
                                "<'row'<'col-sm-12'tr>><'row'<'col-sm-5'i><'col-sm-7'p>>"
                }

                function updateDataTable() {
                    $this.on('drawCallback', function (settings) {
                        feather.replace()
                        $.FincapesCore.helpers.bsUpdate($('tbody tr a#btn-bs-crud'));
                        $.FincapesCore.helpers.bsUpdate($('tbody tr a#btn-bs-delete'));
                    })
                    $this.on('rowCallback', function (table, row, data) {

                    });
                    $this.on('initComplete', function (settings) {
                        feather.replace()
                        var modalId;
                        modalId = $this.data('modal-id') ? $this.data('modal-id') : '#modal';
                        let btnAdd = '<button type="button" ' +
                            'class="btn btn-primary btn-icon-text mb-2 mb-md-0 pt-1 pb-1" ' +
                            'data-form-url="' + $this.attr('data-add-url') +'" id="btn-bs-add" ' +
                            'data-async-update="true" ' +
                            'data-element-id="#' + $this.attr('id') + '" ' +
                            'data-key="table" ' +
                            'data-modal-id="' + modalId  + '" ' +
                            'data-response-url="' + $this.attr('data-response-url') + '">' +
                            '<i class="mdi mdi-plus me-1"></i>' + $this.attr('data-add-btn-title') +
                            '</button>'
                        $('#btn-actions').append(btnAdd);

                        jQuery('#modal').on('hidden.bs.modal', function (e) {
                            $this.DataTable().ajax.reload()
                        })
                        $('#navbarForm').keyup(function () {
                            $this.DataTable().search($(this).val()).draw();
                        })
                        $.FincapesCore.helpers.bsUpdate($('#btn-bs-add'));
                    })

                    AjaxDatatableViewUtils.init({

                        language: {
                            "decimal": ",",
                            "emptyTable": "No data available",
                            "infoFiltered": '(filter from _MAX_ total data',
                            //"info": 'Display _TOTAL_ data entri (_START_ s/d _END_)',
                            "thousands": ".",
                            "paginate": {
                                "next": "<i class='fa fa-angle-right'></i>",
                                "previous": "<i class='fa fa-angle-left'></i>"
                            }
                        }
                    })

                    AjaxDatatableViewUtils.initialize_table(
                        $this, $this.data('ajax-url'),
                        {
                            processing: false,
                            autoWidth: false,
                            full_row_select: false,
                            bFilter: $this.attr('data-show-search') ? $this.data('show-search') : false,
                            bInfo: $this.attr('data-show-total-data') ? $this.data('show-total-data') : false,
                            bPaginate: $this.attr('data-show-pagination') ? $this.data('show-pagination') : false,
                            dom: customDom,
                            scrollX: false
                        }
                    );
                }
                updateDataTable();
            });
        }
    };

    $.FincapesCore.components.datePicker = {
        _baseConfig: {
            inputs: null,
            format: "dd/mm/yyyy",
            keyboardNavigation: true,
            touchAction: true,
            forceParse: false,
            autoclose: false,
            todayHighlight: true,
            language: 'en',
            immediateUpdates: true
        },
        pageCollection: $(),

        init: function (selector, config) {
            this.collection = selector && $(selector).length ? $(selector) : $();
            if (!$(selector).length) return;

            this.config = config && $.isPlainObject(config) ?
                $.extend({}, this._baseConfig, config) : this._baseConfig;

            this.config.itemSelector = selector;

            this.initDatePicker();
            return this.pageCollection;
        },

        initDatePicker: function () {
            var $self = this,
                config = $self.config;

            this.collection.each(function (i, el) {
                var $this = $(el);
                config.inputs = $this.attr('data-inputs') ? $this.data('inputs') : config.inputs
                if ($this.attr('data-inputs')) {
                    config.inputs = $($this.data('inputs'));
                    config.autoclose = $($this.data('auto-close'));
                } else {
                    config.inputs = null;
                    config.autoclose = $this.attr('data-auto-close') ? $this.data('auto-close') : false;
                }
                config.format = $this.data('date-format') ? $this.data('date-format') : config.format;
                $this.each(function () {
                    $this.datepicker(config).bind('keypress', function (e) {
                        e.preventDefault();
                    })
                })
            })
        }
    }

    $.FincapesCore.init();

    $.fn.datepicker.dates['id'] = {
        days: ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', "Jum'at", 'Sabtu'],
        daysShort: ["Min", "Sen", "Sel", "Rab", "Kam", "Jum", "Sab"],
        daysMin: ["Mi", "Sn", "Sl", "Ra", "Ka", "Ju", "Sa"],
        months: ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "Nopember", "Desember"],
        monthsShort: ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agt", "Sep", "Okt", "Nop", "Des"],
        today: "Hari ini",
        clear: "Hapus",
        format: 'dd/mm/yyyy',
        titleFormat: "MM yyyy",
        weekStart: 0
    };
})(jQuery);