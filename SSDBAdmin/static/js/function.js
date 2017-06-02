/**
 * Created by jh on 2017/6/1.
 */

/* change SSDB server */
$(function () {
    $('select[name=SSDBADMIN_SERVER]').change(function(){
        var url = '/ssdbadmin?SSDBADMIN_SERVER=' + $(this).val();
        location.href = url;
        return false;
    })
    
})

function check_all(cb){
    $('#data_list input.cb').each(function(i, e){
        e.checked = cb.checked;
    });
}