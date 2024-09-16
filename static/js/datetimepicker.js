$(document).ready(function () {
  const today = new Date();
  // Tomorrow's date is min and default start date
  const defaultStartDate = today.setDate(today.getDate() + 1);
  // The day after tomorrow's date is min and default end date
  const defaultEndDate = today.setDate(today.getDate() + 1);

  $('#id_start_date').datetimepicker({
    format: 'd/m/Y H:i',
    lazyInit: true,
    step: 30,
    minDate: defaultStartDate,
    defaultDate: defaultStartDate,
    defaultTime: '08:00',
    minTime: '08:00',
    maxTime: '18:30',
    yearStart: today.getFullYear(),
    mask: true,
    dayOfWeekStart: 1,
  });

  $('#id_end_date').datetimepicker({
    format: 'd/m/Y H:i',
    lazyInit: true,
    step: 30,
    minDate: defaultEndDate,
    defaultDate: defaultEndDate,
    defaultTime: '17:00',
    minTime: '08:00',
    maxTime: '18:30',
    yearStart: today.getFullYear(),
    mask: true,
    dayOfWeekStart: 1,
  });

  $('#id_start').datetimepicker({
    format: 'd/m/Y H:i',
    lazyInit: true,
    step: 30,
    minDate: defaultStartDate,
    defaultDate: defaultStartDate,
    defaultTime: '08:00',
    minTime: '08:00',
    maxTime: '18:30',
    yearStart: today.getFullYear(),
    mask: true,
    dayOfWeekStart: 1,
  });
  $('#id_end').datetimepicker({
    format: 'd/m/Y H:i',
    lazyInit: true,
    step: 30,
    minDate: defaultStartDate,
    defaultDate: defaultStartDate,
    defaultTime: '08:00',
    minTime: '08:00',
    maxTime: '18:30',
    yearStart: today.getFullYear(),
    mask: true,
    dayOfWeekStart: 1,
  });
});
