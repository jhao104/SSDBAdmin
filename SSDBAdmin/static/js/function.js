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
