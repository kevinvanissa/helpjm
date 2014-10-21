(function($)
{
    //global properties, depending on current language
    var MonthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    var FirstDayOfWeek = 0;

    //leverage jQuery plugin mechanism
    $.fn.mopCalendar = function(initialDate)
    {
        return this.each(function()
        {
            var $this = $(this);

            var selectedDate = initialDate || new Date();
            var selectedMonth = selectedDate.getMonth();
            var selectedYear = selectedDate.getFullYear();
            
            var isEvent = function(year,month,day)
            {
                var exists;

                 //function to call inside ajax callback 
                function set_exists(x){
                    exists = x;
                }


                //$(document).ready(function(){});
                //$.post('/iseventlist',
                    ////{'year':year,'month':month,'day':day},
                    //{'year':2014,'month':8,'day':31},
                    //function(data){
                        //if (data.answer == "T"){
                            //set_exists(true);
                        //}else{
                            //set_exists(false);
                        //}
                    //});
            $.ajax({
                url: "/iseventlist",
                type: "POST",
                async: false, // set to false so order of operations is correct
                data: {'year':year,'month':month,'day':day},
                success: function(data){
                if(data.answer == "T"){
                    set_exists(true);
                }
                else{
                    set_exists(false);
                }
            }
            });
          
              if(exists == true){
                    return true;
                }else{
                    return false;
                }
            };

            var getValue = function()
            {
                return selectedDate;
            };

            var setValue = function(date)
            {
                if (date == null)
                {
                    selectedDate = null;
                    return;
                }

                selectedDate = new Date(date.getFullYear(), date.getMonth(), date.getDate());
                selectedMonth = getMonth();
                selectedYear = getYear();
                refreshMonthTitle();
                refreshDayTable();
            };

            var getDay = function()
            {
                return selectedDate.getDate();
            };

            var getWeekDay = function()
            {
                return selectedDate.getDay();
            };

            var getMonth = function()
            {
                return selectedDate.getMonth();
            };

            var getYear = function()
            {
                return selectedDate.getFullYear();
            };

            var setSelectedMonth = function(monthNum)
            {
                if (monthNum == -1 && selectedMonth == 0)
                {
                    selectedYear--;
                    selectedMonth = 11;
                }
                else if (monthNum == 12 && selectedMonth == 11)
                {
                    selectedYear++;
                    selectedMonth = 0;
                }
                else if (monthNum >= 0 && monthNum <= 11)
                    selectedMonth = monthNum;
                else
                    return;

                refreshMonthTitle();
                refreshDayTable();
            };

            var setSelectedYear = function(yearNum)
            {
                selectedYear = yearNum;
                refreshMonthTitle();
                refreshDayTable();
            };

            var getContentTable = function () {
                return $this.find('#tabler');
            };

            var refreshDayTable = function () {
                var table = getContentTable();

                var month = selectedMonth;
                var year = selectedYear;

                var startd = new Date(year, month, 1);
                var d1 = FirstDayOfWeek;
                var d2 = startd.getDay();
                var diff = d1 < d2 ? d2 - d1 : d1 + 7;
                startd.setDate(startd.getDate() - diff);

                for (var j = 1; j < 7; j++) {
                    var row = table[0].rows[j];
                    for (var i = 0; i < 7; i++) {
                        var dy = startd.getDate();
                        var wd = startd.getDay();
                        var md = startd.getMonth();
                        var cell = $(row.cells[i]).text(dy);

                        //cell.bind("click",function() {
                            //location = "2?year="+year+"&month="+md+"&day="+dy;
                        //});
                        if( ((j==1 || j == 2) && (dy >= 1 && dy<15)) || ((j==5 || j==6) && (dy<=31 && dy > 15))){
                            //cell.html(function() { return "<a href='findevents?year="+year+"&month="+(month+1)+"&day="+dy+"'>"+$(this).html() +"</a>"; });
                            //alert(isEvent(year,month,dy));
                            if(isEvent(year,month,dy)){
                                cell.html(function() { return "<a href='javascript:showEvents("+year+","+(month+1)+","+dy+")' class='cevents'>"+$(this).html() +"</a>"; });
                            }else{
                                cell.html("<span class='cdays'>"+dy+"</span>");
                            }
                        } //Endif
                        if(j==3 || j==4){
                            if(isEvent(year,month,dy)){
                                cell.html(function() { return "<a href='javascript:showEvents("+year+","+(month+1)+","+dy+")' class='cevents'>"+$(this).html() +"</a>"; });
                            }else{
                                cell.html("<span class='cdays'>"+dy+"</span>");
                            }
                        }//Endif

                        cell.removeClass();
                        if (startd.valueOf() == selectedDate.valueOf())
                            cell.addClass('mopCalendarDaySelected');
                        else if (md != month)
                            cell.addClass('mopCalendarDayOdd');
                        else if (wd == 0 || wd == 6)
                            cell.addClass('mopCalendarDayRed');

                        dy++;
                        startd.setDate(dy);
                    }
                }
            };

            var refreshMonthTitle = function()
            {
                var monthTitle = $('.mopCalendarMonth').text(MonthNames[selectedMonth] + ', ' + selectedYear);
            };


            var onHeaderClick = function(e)
            {
                if (e.target)
                {
                    var target = $(e.target);
                    if (target.hasClass('mopCalendarBtnFirst'))
                        setSelectedYear(selectedYear - 1);
                    else if (target.hasClass('mopCalendarBtnPrevious'))
                        setSelectedMonth(selectedMonth - 1);
                    else if (target.hasClass('mopCalendarBtnNext'))
                        setSelectedMonth(selectedMonth + 1);
                    else if (target.hasClass('mopCalendarBtnLast'))
                        setSelectedYear(selectedYear + 1);
                }
                return false;
            };


            var onBodyClick = function(e)
            {
                if (e.target && e.target.tagName == 'TD')
                {
                    var rowIndex = e.target.parentElement.rowIndex;
                    var month = selectedMonth;
                    var year = selectedYear;
                    var day = parseInt($(e.target).text());

                    if (rowIndex <= 1 && day >= 20)
                        month--;
                    else if (rowIndex >= 5 && day <= 15)
                        month++;

                    setValue(new Date(year, month, day));
                }
            };


            var onFooterClick = function(e)
            {
                if (e.target && e.target.tagName == 'BUTTON')
                {
                    var $target = $(e.target);
                    if ($target.hasClass('mopCalendarBtnToday'))
                        setValue(new Date());
                }
                return false;
            };


            //attach click events to the different section
            $('.mopCalendarHeader').on('click', onHeaderClick);
            $('.mopCalendarBody').on('click', onBodyClick);
            $('.mopCalendarFooter').on('click', onFooterClick);

            //disable drag
            $this.on('selectstart dragstart', function (e) { e.preventDefault(); });

            //public method call
            this.setValue = (function (value) {
                setValue(value);
            })(initialDate);

        });

    };
} (jQuery));
    

