class BlockWidget {
    constructor(block_choices, block_area, block_modal) {
        this.block_choices = block_choices;

        this.block_area = block_area;
        this.block_area.on('click', '.close', $.proxy(this.destroy_option, this));

        this.block_modal = block_modal;
        this.block_modal.on('click', '.block-option', $.proxy(this.update_modal_option, this));
        this.block_modal.on('show.bs.modal', $.proxy(this.modal_show, this));
        this.block_modal.on('hide.bs.modal', $.proxy(this.modal_hide, this));

        this.render_widget();
    }

    destroy_option(event) {
        var target = $(event.target);
        var parentdiv = target.parent().parent();
        var index = parentdiv.data('optionindex');
        this.block_choices[index].selected = false;

        this.render_widget();
    }

    modal_show() {
        this.render_modal();
    }

    modal_hide() {
        this.render_widget();
    }

    update_modal_option(event) {
        var target = $(event.target);
        var index = target.data('optionindex');
        this.block_choices[index].selected = !this.block_choices[index].selected;
        this.render_modal();
    }

    render_modal() {

        var result = "";
        this.block_choices.map(function(element, index) {
                result += `
                <div class="alert ${element.selected ? 'alert-success' : ''} block-option" data-optionindex="${index}">
                ${element.block_name}
                <small>${element.geodataset_name}</small>
                </div>`;
        });

        this.block_modal.find('#modal-blocks').html(result);
    }

    render_widget() {
        var result = "";

        this.block_choices.map(function(element, index) {
            if (element.selected) {
                result += `
                <div class="alert alert-success block-option" data-optionindex="${index}">
                <button type="button" class="close" aria-label="Close">
                <span aria-hidden="true">&times;</span></button>${element.block_name}
                <small>${element.geodataset_name}</small>
                <input type="hidden" name="blocks" value="${element.block_key}" />
                </div>`;
            }
        });

        this.block_area.html(result);
    }
}


$(document).ready(function() {
    var block_area = $('#block-area'),
        block_modal = $('#block-modal');
    new BlockWidget(window.block_choices, block_area, block_modal);
});
