import React from 'react';
import { Calendar, dateFnsLocalizer } from 'react-big-calendar';
import { format, parse, startOfWeek, getDay } from 'date-fns';
import { enUS } from 'date-fns/locale/en-US';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import type { Meeting } from '../services/api';

const locales = {
  'en-US': enUS,
};

const localizer = dateFnsLocalizer({
  format,
  parse,
  startOfWeek,
  getDay,
  locales,
});

interface MeetingCalendarProps {
  meetings: Meeting[];
}

export const MeetingCalendar: React.FC<MeetingCalendarProps> = ({ meetings }) => {
  // Convert meetings to react-big-calendar event format
  const events = meetings.map(meeting => {
    const start = new Date(meeting.date);
    const end = new Date(start.getTime() + meeting.duration_minutes * 60000);
    return {
      title: meeting.title,
      start,
      end,
      resource: meeting,
    };
  });

  // Find the most recent meeting date to set as the default date
  // Since our mock data goes up to June 2026, we should default the view to that period
  const defaultDate = meetings.length > 0 
    ? new Date(Math.max(...meetings.map(m => new Date(m.date).getTime())))
    : new Date();

  return (
    <div className="card" style={{ marginBottom: '2rem' }}>
      <div className="card-header">
        <h2 className="card-title">Meeting Schedule</h2>
      </div>
      <div style={{ height: '500px', marginTop: '1rem' }}>
        <Calendar
          localizer={localizer}
          events={events}
          startAccessor="start"
          endAccessor="end"
          style={{ height: '100%' }}
          defaultDate={defaultDate}
          defaultView="month"
          views={['month', 'week', 'day', 'agenda']}
          popup
        />
      </div>
    </div>
  );
};
