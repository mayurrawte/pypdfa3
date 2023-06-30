ps_content_template = '''% Define an ICC profile :
/ICCProfile (/usr/share/ghostscript/{gs_version}/iccprofiles/default_rgb.icc) def

% Define an OutputConditionIdentifier :
/OutputConditionIdentifier (default_rgb) def

% Create a PDF stream object to hold the XML invoice :
[ /_objdef {{InvoiceStream}} /type /stream /OBJ pdfmark

% Add the required entries to that stream dictionary :
[ {{InvoiceStream}} << /Type /EmbeddedFile /Subtype (text/xml) cvn /Params << /ModDate (D:20130121081433+01'00') >> >> /PUT pdfmark

% Read the XML invoice data from the file and store it in the PDF stream :
[ {{InvoiceStream}} ({xml_path}) (r) file /PUT pdfmark

% Close the PDF stream :
[ {{InvoiceStream}} /CLOSE pdfmark

% Create a PDF file specification dictionary to hold the file info :
[ /_objdef {{InvoiceFile}} /type /dict /OBJ pdfmark

% Add the required entries to that file specification dictionary :
[ {{InvoiceFile}} <<
    /Type /Filespec
    /F ({xml_filename})
    /EF << /F {{InvoiceStream}} >>
>> /PUT pdfmark


% Associate the file specification with the PDF document :
[/Root <<
    /Names << /EmbeddedFiles << /Names [ ({xml_filename}) {{InvoiceFile}} ] >> >>
>> /pdfmark


% Create an annotation to display the attachment in the PDF viewer:
[{{Catalog}} <<
    /Names << /EmbeddedFiles << /Names [ ({xml_filename}) {{InvoiceFile}} ] >> >>
    /ViewerPreferences <<
        /DisplayDocTitle true
    >>
    /PageLayout /SinglePage
    /PageMode /UseAttachments
>> /PUT pdfmark'''
