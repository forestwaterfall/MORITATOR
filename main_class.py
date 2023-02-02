import wx
import wx.xrc

class main_class ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = 'MORITATOR', pos = wx.DefaultPosition, size = wx.Size( 750,500 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL|wx.MINIMIZE_BOX )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.Colour( '#e0f9b5' ) )
        self.SetForegroundColour( wx.Colour( '#212121' ) )

        outer = wx.BoxSizer( wx.VERTICAL )

        outer.SetMinSize( wx.Size( 750,500 ) )
        inner = wx.BoxSizer( wx.VERTICAL )

        inner.SetMinSize( wx.Size( 750,500 ) )
        head = wx.BoxSizer( wx.VERTICAL )

        head.SetMinSize( wx.Size( 750,110 ) )
        head_inner = wx.BoxSizer( wx.HORIZONTAL )
        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"MORITATOR by forestwaterfall                                                                 ", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        head_inner.Add( self.m_staticText1, 0, wx.ALL, 5 )

        self.m_staticText1.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Helvetica" ) )
        self.is_multiple_checkbox = wx.CheckBox( self, wx.ID_ANY, u"Track Multiple Satellite", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
        head_inner.Add( self.is_multiple_checkbox, 0, wx.ALL, 5 )
        head.Add( head_inner, 0, wx.EXPAND, 20 )

        tracking_name = wx.BoxSizer( wx.HORIZONTAL )

        tracking_name.SetMinSize( wx.Size( 750,-1 ) )
        self.tracking = wx.StaticText( self, wx.ID_ANY, u"\n               Now Tracking ", wx.Point( -1,10 ), wx.Size( 300,50 ), wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_RIGHT )
        self.tracking.Wrap( -1 )

        self.tracking.SetFont( wx.Font( 18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Lucida Grande" ) )

        tracking_name.Add( self.tracking, 0, wx.ALL, 5 )

        self.tracking_satellite = wx.StaticText( self, wx.ID_ANY, self.sat_name, wx.Point( 450,-1 ), wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.tracking_satellite.Wrap( -1 )

        self.tracking_satellite.SetFont( wx.Font( 48, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Lucida Grande" ) )

        tracking_name.Add( self.tracking_satellite, 0, wx.ALL, 5 )


        head.Add( tracking_name, 1, wx.EXPAND, 5 )


        inner.Add( head, 1, wx.EXPAND, 5 )

        body = wx.BoxSizer( wx.HORIZONTAL )

        body.SetMinSize( wx.Size( 750,375 ) )
        body_left = wx.BoxSizer( wx.VERTICAL )

        body_left.SetMinSize( wx.Size( 500,-1 ) )
        setting = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

        wSizer10 = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

        self.m_staticText74 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText74.Wrap( -1 )

        self.m_staticText74.SetMinSize( wx.Size( 20,-1 ) )

        wSizer10.Add( self.m_staticText74, 0, wx.ALL, 5 )


        setting.Add( wSizer10, 1, wx.EXPAND, 5 )

        satellite_box = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"Satellite", wx.DefaultPosition, wx.Size( 140,-1 ), 0 )
        self.m_staticText5.Wrap( -1 )

        satellite_box.Add( self.m_staticText5, 0, wx.ALL, 5 )

        #self.satellite_choiceChoices = [ u"ISS", u"NEXUS" ]
        self.satellite_choice = wx.Choice( self, wx.ID_ANY, wx.Point( 100,-1 ), wx.DefaultSize, self.satellite_choiceChoices, 0 )
        self.satellite_choice.SetSelection( self.sat_num )
        self.satellite_choice.SetMinSize( wx.Size( 120,-1 ) )

        satellite_box.Add( self.satellite_choice, 0, wx.ALL, 5 )

        bSizer131 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText71 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText71.Wrap( -1 )

        self.m_staticText71.SetMinSize( wx.Size( 60,-1 ) )

        bSizer131.Add( self.m_staticText71, 0, wx.ALL, 5 )

        self.set_satellite_b = wx.Button( self, wx.ID_ANY, u"SET", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
        bSizer131.Add( self.set_satellite_b, 0, wx.ALL, 5 )


        satellite_box.Add( bSizer131, 1, wx.EXPAND, 5 )


        setting.Add( satellite_box, 1, wx.EXPAND, 5 )

        norad_id_box = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u"NORAD ID", wx.DefaultPosition, wx.Size( 140,-1 ), 0 )
        self.m_staticText6.Wrap( -1 )

        norad_id_box.Add( self.m_staticText6, 0, wx.ALL, 5 )

        self.norad_id_input = wx.TextCtrl( self, wx.ID_ANY, self.norad_id, wx.DefaultPosition, wx.DefaultSize, 0 )
        norad_id_box.Add( self.norad_id_input, 0, wx.ALL, 5 )

        bSizer13 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 45,-1 ), 0 )
        self.m_staticText7.Wrap( -1 )

        bSizer13.Add( self.m_staticText7, 0, wx.ALL, 5 )

        self.set_norad_b = wx.Button( self, wx.ID_ANY, u"SET", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
        bSizer13.Add( self.set_norad_b, 0, wx.ALL, 5 )


        norad_id_box.Add( bSizer13, 1, wx.EXPAND, 5 )


        setting.Add( norad_id_box, 1, wx.EXPAND, 5 )

        comport_box = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u"COM PORT", wx.DefaultPosition, wx.Size( 140,-1 ), 0 )
        self.m_staticText8.Wrap( -1 )

        comport_box.Add( self.m_staticText8, 0, wx.ALL, 5 )

        #self.com_port_choiceChoices = [ u"COM20" ]
        self.com_port_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, self.com_port_choiceChoices, 0 )
        self.com_port_choice.SetStringSelection( self.port )
        self.com_port_choice.SetMinSize( wx.Size( 120,-1 ) )

        comport_box.Add( self.com_port_choice, 0, wx.ALL, 5 )

        bSizer1311 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText711 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText711.Wrap( -1 )

        self.m_staticText711.SetMinSize( wx.Size( 60,-1 ) )

        bSizer1311.Add( self.m_staticText711, 0, wx.ALL, 5 )

        self.set_comport_b = wx.Button( self, wx.ID_ANY, u"SET", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
        bSizer1311.Add( self.set_comport_b, 0, wx.ALL, 5 )


        comport_box.Add( bSizer1311, 1, wx.EXPAND, 5 )


        setting.Add( comport_box, 1, wx.EXPAND, 5 )


        body_left.Add( setting, 1, wx.EXPAND, 5 )

        direction = wx.BoxSizer( wx.VERTICAL )

        wSizer1 = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

        bSizer34 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText31 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,15 ), 0 )
        self.m_staticText31.Wrap( -1 )

        bSizer34.Add( self.m_staticText31, 0, wx.ALL, 5 )

        self.m_staticText26 = wx.StaticText( self, wx.ID_ANY, u"ANTENNA", wx.Point( -1,-1 ), wx.Size( 150,-1 ), wx.ALIGN_CENTER_HORIZONTAL )
        self.m_staticText26.Wrap( -1 )

        self.m_staticText26.SetFont( wx.Font( 24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Lucida Grande" ) )
        self.m_staticText26.SetMinSize( wx.Size( 195,50 ) )

        bSizer34.Add( self.m_staticText26, 0, wx.ALL, 5 )


        wSizer1.Add( bSizer34, 1, wx.EXPAND, 5 )

        bSizer32 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText27 = wx.StaticText( self, wx.ID_ANY, u"Elevation", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.m_staticText27.Wrap( -1 )

        self.m_staticText27.SetMinSize( wx.Size( 130,-1 ) )

        bSizer32.Add( self.m_staticText27, 0, wx.ALL, 5 )

        self.antenna_ele = wx.StaticText( self, wx.ID_ANY, u"xxxx", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.antenna_ele.Wrap( -1 )

        self.antenna_ele.SetFont( wx.Font( 18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Lucida Grande" ) )
        self.antenna_ele.SetBackgroundColour( wx.Colour( '#FFF6F6' ) )
        self.antenna_ele.SetMinSize( wx.Size( 130,25 ) )

        bSizer32.Add( self.antenna_ele, 0, wx.ALL, 5 )


        wSizer1.Add( bSizer32, 1, wx.EXPAND, 5 )

        bSizer33 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText29 = wx.StaticText( self, wx.ID_ANY, u"Azimuth", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.m_staticText29.Wrap( -1 )

        self.m_staticText29.SetMinSize( wx.Size( 130,-1 ) )

        bSizer33.Add( self.m_staticText29, 0, wx.ALL, 5 )

        self.antenna_azi = wx.StaticText( self, wx.ID_ANY, u"xxxx", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.antenna_azi.Wrap( -1 )

        self.antenna_azi.SetFont( wx.Font( 18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Lucida Grande" ) )
        self.antenna_azi.SetBackgroundColour( wx.Colour( '#FFF6F6' ) )
        self.antenna_azi.SetMinSize( wx.Size( 130,25 ) )

        bSizer33.Add( self.antenna_azi, 0, wx.ALL, 5 )


        wSizer1.Add( bSizer33, 1, wx.EXPAND, 5 )


        direction.Add( wSizer1, 1, wx.EXPAND, 5 )

        wSizer11 = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

        bSizer341 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText311 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,15 ), 0 )
        self.m_staticText311.Wrap( -1 )

        bSizer341.Add( self.m_staticText311, 0, wx.ALL, 5 )

        self.m_staticText261 = wx.StaticText( self, wx.ID_ANY, u"SATELLITE", wx.Point( -1,-1 ), wx.Size( 200,-1 ), wx.ALIGN_CENTER_HORIZONTAL )
        self.m_staticText261.Wrap( -1 )

        self.m_staticText261.SetFont( wx.Font( 24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Lucida Grande" ) )
        self.m_staticText261.SetMinSize( wx.Size( 195,50 ) )

        bSizer341.Add( self.m_staticText261, 0, wx.ALL, 5 )


        wSizer11.Add( bSizer341, 1, wx.EXPAND, 5 )

        bSizer321 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText271 = wx.StaticText( self, wx.ID_ANY, u"Elevation", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.m_staticText271.Wrap( -1 )

        self.m_staticText271.SetMinSize( wx.Size( 130,-1 ) )

        bSizer321.Add( self.m_staticText271, 0, wx.ALL, 5 )

        self.sat_ele = wx.StaticText( self, wx.ID_ANY, u"xxxx", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.sat_ele.Wrap( -1 )

        self.sat_ele.SetFont( wx.Font( 18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Lucida Grande" ) )
        self.sat_ele.SetBackgroundColour( wx.Colour( '#FFF6F6' ) )
        self.sat_ele.SetMinSize( wx.Size( 130,25 ) )

        bSizer321.Add( self.sat_ele, 0, wx.ALL, 5 )


        wSizer11.Add( bSizer321, 1, wx.EXPAND, 5 )

        bSizer331 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText291 = wx.StaticText( self, wx.ID_ANY, u"Azimuth", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.m_staticText291.Wrap( -1 )

        self.m_staticText291.SetMinSize( wx.Size( 130,-1 ) )

        bSizer331.Add( self.m_staticText291, 0, wx.ALL, 5 )

        self.sat_azi = wx.StaticText( self, wx.ID_ANY, u"xxxx", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.sat_azi.Wrap( -1 )

        self.sat_azi.SetFont( wx.Font( 18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Lucida Grande" ) )
        self.sat_azi.SetBackgroundColour( wx.Colour( '#FFF6F6' ) )
        self.sat_azi.SetMinSize( wx.Size( 130,25 ) )

        bSizer331.Add( self.sat_azi, 0, wx.ALL, 5 )


        wSizer11.Add( bSizer331, 1, wx.EXPAND, 5 )


        direction.Add( wSizer11, 1, wx.EXPAND, 5 )

        wSizer12 = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

        bSizer342 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText312 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,15 ), 0 )
        self.m_staticText312.Wrap( -1 )

        bSizer342.Add( self.m_staticText312, 0, wx.ALL, 5 )

        self.m_staticText262 = wx.StaticText( self, wx.ID_ANY, u"NEXT PASS", wx.Point( -1,-1 ), wx.Size( 200,-1 ), wx.ALIGN_CENTER_HORIZONTAL )
        self.m_staticText262.Wrap( -1 )

        self.m_staticText262.SetFont( wx.Font( 24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Lucida Grande" ) )
        self.m_staticText262.SetMinSize( wx.Size( 195,50 ) )

        bSizer342.Add( self.m_staticText262, 0, wx.ALL, 5 )


        wSizer12.Add( bSizer342, 1, wx.EXPAND, 5 )

        bSizer322 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText272 = wx.StaticText( self, wx.ID_ANY, u"RISE", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.m_staticText272.Wrap( -1 )

        self.m_staticText272.SetMinSize( wx.Size( 130,-1 ) )

        bSizer322.Add( self.m_staticText272, 0, wx.ALL, 5 )

        self.next_rise = wx.StaticText( self, wx.ID_ANY, u"xxxx", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.next_rise.Wrap( -1 )

        self.next_rise.SetFont( wx.Font( 18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Lucida Grande" ) )
        self.next_rise.SetBackgroundColour( wx.Colour( '#FFF6F6' ) )
        self.next_rise.SetMinSize( wx.Size( 130,25 ) )

        bSizer322.Add( self.next_rise, 0, wx.ALL, 2 )


        wSizer12.Add( bSizer322, 1, wx.EXPAND, 2 )

        bSizer332 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText292 = wx.StaticText( self, wx.ID_ANY, u"SET", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.m_staticText292.Wrap( -1 )

        self.m_staticText292.SetMinSize( wx.Size( 130,-1 ) )

        bSizer332.Add( self.m_staticText292, 0, wx.ALL, 5 )

        self.next_set = wx.StaticText( self, wx.ID_ANY, u"xxxx", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.next_set.Wrap( -1 )

        self.next_set.SetFont( wx.Font( 18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Lucida Grande" ) )
        self.next_set.SetBackgroundColour( wx.Colour( '#FFF6F6' ) )
        self.next_set.SetMinSize( wx.Size( 130,25 ) )

        bSizer332.Add( self.next_set, 0, wx.ALL, 2 )


        wSizer12.Add( bSizer332, 1, wx.EXPAND, 2 )


        direction.Add( wSizer12, 1, wx.EXPAND, 2 )


        body_left.Add( direction, 1, wx.EXPAND, 2 )


        body.Add( body_left, 1, wx.EXPAND, 2 )

        self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,300 ), wx.LI_HORIZONTAL )
        self.m_staticline1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        self.m_staticline1.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )
        self.m_staticline1.SetMinSize( wx.Size( 10,700 ) )

        body.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 2 )

        body_right = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

        bSizer29 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer29.SetMinSize( wx.Size( -1,200 ) )
        bSizer28 = wx.BoxSizer( wx.VERTICAL )

        aos1 = wx.BoxSizer( wx.VERTICAL )

        self.aos = wx.StaticText( self, wx.ID_ANY, u"AOS", wx.DefaultPosition, wx.Size( 200,-1 ), wx.ALIGN_CENTER_HORIZONTAL )
        self.aos.Wrap( -1 )

        self.aos.SetFont( wx.Font( 18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Lucida Grande" ) )

        aos1.Add( self.aos, 0, wx.ALL, 5 )

        self.aos_time = wx.StaticText( self, wx.ID_ANY, u"xxxxx\nxxxxx", wx.DefaultPosition, wx.Size( 200,50 ), wx.ALIGN_CENTER_HORIZONTAL )
        self.aos_time.Wrap( -1 )

        self.aos_time.SetFont( wx.Font( 18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Lucida Grande" ) )
        self.aos_time.SetBackgroundColour( wx.Colour( '#FFF6F6' ) )

        aos1.Add( self.aos_time, 0, wx.ALL, 5 )


        bSizer28.Add( aos1, 1, wx.EXPAND, 5 )

        los = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText181 = wx.StaticText( self, wx.ID_ANY, u"LOS", wx.DefaultPosition, wx.Size( 200,-1 ), wx.ALIGN_CENTER_HORIZONTAL )
        self.m_staticText181.Wrap( -1 )

        self.m_staticText181.SetFont( wx.Font( 18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Lucida Grande" ) )

        los.Add( self.m_staticText181, 0, wx.ALL, 5 )

        self.los_time = wx.StaticText( self, wx.ID_ANY, u"xxxxx\nxxxxx", wx.DefaultPosition, wx.Size( 200,50 ), wx.ALIGN_CENTER_HORIZONTAL )
        self.los_time.Wrap( -1 )

        self.los_time.SetFont( wx.Font( 18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Lucida Grande" ) )
        self.los_time.SetBackgroundColour( wx.Colour( '#FFF6F6' ) )

        los.Add( self.los_time, 0, wx.ALL, 5 )


        bSizer28.Add( los, 1, wx.EXPAND, 5 )


        bSizer29.Add( bSizer28, 1, wx.EXPAND, 5 )


        body_right.Add( bSizer29, 1, wx.EXPAND, 5 )

        bSizer61 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer61.SetMinSize( wx.Size( -1,30 ) )
        self.m_staticText14 = wx.StaticText( self, wx.ID_ANY, u"ROUND ROTATION:", wx.Point( -1,-1 ), wx.Size( 145,-1 ), wx.ALIGN_LEFT )
        self.m_staticText14.Wrap( -1 )

        self.m_staticText14.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Lucida Grande" ) )

        bSizer61.Add( self.m_staticText14, 0, wx.ALL, 5 )

        self.daisenkai_yesno_text = wx.StaticText( self, wx.ID_ANY, u"", wx.DefaultPosition, wx.Size( -1,-1 ), wx.ALIGN_LEFT )
        self.daisenkai_yesno_text.Wrap( -1 )

        self.daisenkai_yesno_text.SetFont( wx.Font( 14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Lucida Grande" ) )
        self.daisenkai_yesno_text.SetForegroundColour( wx.Colour( 0, 0, 0 ) )

        bSizer61.Add( self.daisenkai_yesno_text, 0, wx.ALL, 5 )


        body_right.Add( bSizer61, 1, wx.EXPAND, 5 )

        bSizer13111 = wx.BoxSizer( wx.HORIZONTAL )

        self.daisenkai_b = wx.Button( self, wx.ID_ANY, u"MANUAL", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
        self.daisenkai_b.SetFont( wx.Font( 17, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Lucida Grande" ) )
        self.daisenkai_b.SetMinSize( wx.Size( 100,30 ) )

        bSizer13111.Add( self.daisenkai_b, 0, wx.ALL, 5 )

        bSizer13111.SetMinSize( wx.Size( -1,20 ) )
        self.m_staticText7111 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 0,-1 ), 0 )
        self.m_staticText7111.Wrap( -1 )

        bSizer13111.Add( self.m_staticText7111, 0, wx.ALL, 0 )

        self.daisenkai_b2 = wx.Button( self, wx.ID_ANY, u"DISABLE", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
        self.daisenkai_b2.SetFont( wx.Font( 17, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Lucida Grande" ) )
        self.daisenkai_b2.SetMinSize( wx.Size( 100,30 ) )

        bSizer13111.Add( self.daisenkai_b2, 0, wx.ALL, 5 )



        body_right.Add( bSizer13111, 1, wx.EXPAND, 5 )

        self.now_daisenkai_text = wx.StaticText( self, wx.ID_ANY, u"AUTO ROTATION (default)", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.now_daisenkai_text.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Lucida Grande" ) )
        self.now_daisenkai_text.Wrap( -1 )

        self.now_daisenkai_text.SetMinSize( wx.Size( 200,20 ) )

        body_right.Add( self.now_daisenkai_text, 0, wx.ALL, 5 )

        bSizer131111 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer131111.SetMinSize( wx.Size( -1,20 ) )
        self.m_staticText71111 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 0,-1 ), 0 )
        self.m_staticText71111.Wrap( -1 )

        bSizer131111.Add( self.m_staticText71111, 0, wx.ALL, 2 )

        self.set_90_b = wx.Button( self, wx.ID_ANY, u"SET 90 and QUIT", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
        self.set_90_b.SetFont( wx.Font( 18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Lucida Grande" ) )
        self.set_90_b.SetMinSize( wx.Size( 190,30 ) )

        bSizer131111.Add( self.set_90_b, 0, wx.ALL, 5 )


        body_right.Add( bSizer131111, 1, wx.EXPAND, 5 )


        body.Add( body_right, 1, wx.EXPAND, 5 )


        inner.Add( body, 1, wx.EXPAND, 5 )


        outer.Add( inner, 1, wx.EXPAND, 5 )


        self.SetSizer( outer )
        self.Layout()

        self.Centre( wx.BOTH )


    def __del__( self ):
        pass
