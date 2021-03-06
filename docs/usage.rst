========
Usage
========

To use django-sheets, you need to have a key to a publically-accessible 
Google Sheets spreadsheet. To find it, open your sheet and select
*File* -> *Share*.
Click *Get sharable link* from the dialog. You'll find the 44-character key as
part of the URL.

For example, the sample link ``https://docs.google.com/spreadsheets/d/1bJNR7SLqpzWJNvstNcFR4gtS-M7Bmn0D1X2lGTJPvGM/pubhtml``
has key ``1bJNR7SLqpzWJNvstNcFR4gtS-M7Bmn0D1X2lGTJPvGM``

Load the django-sheets template tags in your template::

    {% load sheets %}

Assign the CSV data to a variable using the ``{% csv %}`` tag::

    {% csv <key> as <variable_name> %}

Try it using the sample key above::

    {% load sheets %}
    {% csv "1uPsdcGUnUsf3d2xGHRGUUb7_k5IQPtBvfQY61u8Z8wE" as data %}
    <table>
        <thead>
            <tr>
            {% for header in data.headers %}
                <th>{{ header }}</th>
            {% endfor %}
            </tr>
        </thead>
        <tbody>
            {% for row in data.rows %}
            <tr>
                {% for cell in row %}
                    <td>{{ cell }}</td>
                {% endfor %}
            </tr>
            {% endfor %}
        </tbody>
    </table>
    

View the output, you should see

=================================  =======================  ====================  =======================
**Origin (English)**               **Name (English)**       **Origin (Native)**   **Name (Native)**
Australia                          Nicole Kidman            Australia             Nicole Kidman
Austria                            Johann Strauss           Österreich            Johann Strauß
Belgium (Flemish)                  Rene Magritte            België                René Magritte
Belgium (French)                   Rene Magritte            Belgique              René Magritte
Belgium (German)                   Rene Magritte            Belgien               René Magritte
=================================  =======================  ====================  =======================
