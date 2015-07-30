/**
 * Created by irakli on 5/14/15.
 */
NS_DJANGO_JCROP = {};
NS_DJANGO_JCROP.MAX_WIDTH = 400;
NS_DJANGO_JCROP.MAX_HEIGHT = 200;
NS_DJANGO_JCROP.getFileReader = function (target) {
    var oFReader = new FileReader();
    oFReader.readAsDataURL(target.files[0]);
    oFReader.onload = function (oFREvent) {
        document.getElementById(target.id + '_preview').src = oFREvent.target.result;
        var item = $('#' + target.id + '_preview')[0];
        NS_DJANGO_JCROP.destroyJcrop(target.id);
        NS_DJANGO_JCROP.jcrop(item, target.id);
    };
    return oFReader;
};


NS_DJANGO_JCROP.on_ratio_chnage = function (e) {
    var target = e.target;
    var id = $(target).attr('jcrop_parent_id');
    var width = $('#' + id + '_ratio [name=width]')[0].value;
    var height = $('#' + id + '_ratio [name=height]')[0].value;
    var api = NS_DJANGO_JCROP.JCROP_API_LIST[id];
    if (api) {
        api.setOptions(
            {
                aspectRatio: width / height
            }
        )
    }
};


NS_DJANGO_JCROP.get_aspect_ratio_control = function (w, h, p_id) {
    var container = document.createElement('div');
    container.id = p_id + '_ratio';

    var width = document.createElement('input');
    width.value = w;
    $(width).attr('jcrop_parent_id', p_id);
    $(width).attr('name', 'width');
    $(width).on('keyup', NS_DJANGO_JCROP.on_ratio_chnage);

    var height = document.createElement('input');
    height.value = h;
    $(height).attr('jcrop_parent_id', p_id);
    $(height).attr('name', 'height');
    $(height).on('keyup', NS_DJANGO_JCROP.on_ratio_chnage);

    var quality = document.createElement('input');
    quality.value = 100;
    $(quality).attr('type', 'range');
    $(quality).attr('min', '0');
    $(quality).attr('max', '100');
    $(quality).attr('jcrop_parent_id', p_id);
    $(quality).attr('name', 'quality');
    $(quality).on('keyup', NS_DJANGO_JCROP.on_ratio_chnage);

    $(container).append('<span> width </span>');
    $(container).append(width);
    $(container).append('<span> height </span>');
    $(container).append(height);
    $(container).append('<span> quality </span>');
    $(container).append(quality);
    return container;
};


NS_DJANGO_JCROP.jcrop_init = function (item) {
    item = item.target;
    NS_DJANGO_JCROP.getFileReader(item);
};


NS_DJANGO_JCROP.jcrop_onready = function () {
    $('.jcrop_image_input').each(function (index, item) {
        var parent = $(item).parent()[0];

        var image = new Image();
        image.style.maxWidth = '400px';
        image.style.maxHeight = '200px';
        image.id = item.id + "_preview";

        var width_ratio = Number($(item).attr('jcrop_width_ratio'));
        var height_ratio = Number($(item).attr('jcrop_height_ratio'));

        $(image).attr('jcrop_width_ratio', width_ratio);
        $(image).attr('jcrop_height_ratio', height_ratio);
        $(image).addClass('jcrop_preview');
        $(parent).append(image);

        var input = document.createElement('input');
        input.id = item.id + '_hidden';
        $(input).attr('type', 'hidden');
        $(input).attr('name', $(item).attr('name') + '_jcrop');
        $(parent).append(input);
        $(parent).append(NS_DJANGO_JCROP.get_aspect_ratio_control(width_ratio, height_ratio, item.id));

        if ($(item).attr('jcrop_url') !== 'undefined') {
            var anchor = document.createElement('a');
            $(anchor).attr('href', $(item).attr('jcrop_url'));
            $(anchor).text($(item).attr('jcrop_url'));
            $(anchor).attr('download', '');
            $(parent).append(anchor);
            image.src = $(item).attr('jcrop_url');

            NS_DJANGO_JCROP.jcrop(image, item.id);
        }

        $(item).on('change', NS_DJANGO_JCROP.jcrop_init)
    });
};


NS_DJANGO_JCROP.on_change = function (item, c) {
    var id = '#' + item.id.substring(0, item.id.length - '_preview'.length);
    var quality = Number($(id + '_ratio [name=quality]')[0].value);
    c['actual_width'] = $(item).width();
    c['actual_height'] = $(item).height();
    c['quality'] = quality;
    $(id + '_hidden').attr('value', JSON.stringify(c));
};

NS_DJANGO_JCROP.JCROP_API_LIST = [];


NS_DJANGO_JCROP.jcrop = function (image, apiKey) {
    var ratio = Number($("#" + image.id).attr('jcrop_width_ratio')) / Number(($("#" + image.id).attr('jcrop_height_ratio')));
    //

    var crop = function () {
        $("#" + image.id).Jcrop({
            onChange: function (c) {
                NS_DJANGO_JCROP.on_change(image, c);
            },
            aspectRatio: ratio,
            setSelect: [0, 0, 100, 100],
            allowSelect: false
        }, function () {
            this.imgNode = image;
            NS_DJANGO_JCROP.JCROP_API_LIST[apiKey] = this;
            var width = $(image).width();
            var height = width / ratio;
            this.setOptions({setSelect: [0, 0, width, height]});
            console.log(this.setSelect);
        });
    };
    crop();

    NS_DJANGO_JCROP.destroyJcrop(apiKey, crop);
};
NS_DJANGO_JCROP.destroyJcrop = function (apiKey, callback) {
    var api = NS_DJANGO_JCROP.JCROP_API_LIST[apiKey];
    if (api) {
        api.destroy(callback);
    }
};
$(document).ready(
    function () {
        NS_DJANGO_JCROP.jcrop_onready();
    }
);

