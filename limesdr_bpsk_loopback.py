#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Ettus B205 Loopback FSK Test
# Author: Bradford MacEwen
# Copyright: 2024
# Description: Sends data with FSK through Ettus SDR
# GNU Radio version: 3.8.5.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
import math
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
from hdlc_framer_with_preamble import hdlc_framer_with_preamble  # grc-generated hier_block
from nrzs_line_coding import nrzs_line_coding  # grc-generated hier_block
from trxv_uplink_fsk_modulator import trxv_uplink_fsk_modulator  # grc-generated hier_block
import limesdr

from gnuradio import qtgui

class limesdr_bpsk_loopback(gr.top_block, Qt.QWidget):

    def __init__(self, baud_rate=1200, equ_gain=0.01, excess_bw=0.35, fc_rx=436.83e6, fc_tx=145.91e6, loop_bw=0.0628, rx_gain_default=56, sps=160, tx_gain_56=56):
        gr.top_block.__init__(self, "Ettus B205 Loopback FSK Test")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Ettus B205 Loopback FSK Test")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "limesdr_bpsk_loopback")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Parameters
        ##################################################
        self.baud_rate = baud_rate
        self.equ_gain = equ_gain
        self.excess_bw = excess_bw
        self.fc_rx = fc_rx
        self.fc_tx = fc_tx
        self.loop_bw = loop_bw
        self.rx_gain_default = rx_gain_default
        self.sps = sps
        self.tx_gain_56 = tx_gain_56

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = baud_rate*sps
        self.tx_gain = tx_gain = tx_gain_56
        self.rx_gain = rx_gain = rx_gain_default
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(1.0,samp_rate,2*samp_rate/sps,excess_bw,11*sps)
        self.fc_tx_gui = fc_tx_gui = 145.91e6
        self.bpsk_obj = bpsk_obj = digital.constellation_bpsk().base()

        ##################################################
        # Blocks
        ##################################################
        self._rx_gain_range = Range(0, 60, 1, rx_gain_default, 200)
        self._rx_gain_win = RangeWidget(self._rx_gain_range, self.set_rx_gain, 'rx_gain', "counter_slider", float)
        self.top_layout.addWidget(self._rx_gain_win)
        self._tx_gain_range = Range(0, 60, 1, tx_gain_56, 200)
        self._tx_gain_win = RangeWidget(self._tx_gain_range, self.set_tx_gain, 'tx_gain', "counter_slider", int)
        self.top_layout.addWidget(self._tx_gain_win)
        self.trxv_uplink_fsk_modulator_0 = trxv_uplink_fsk_modulator(
            samp_rate=samp_rate,
            sps=sps,
        )
        self.root_raised_cosine_filter_1 = filter.fir_filter_fff(
            1,
            firdes.root_raised_cosine(
                1,
                samp_rate,
                2*samp_rate/sps,
                0.0035,
                160))
        self.qtgui_waterfall_sink_x_0_0 = qtgui.waterfall_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            fc_tx, #fc
            10000, #bw
            "TX", #name
            1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0_0.set_intensity_range(-110, -20)

        self._qtgui_waterfall_sink_x_0_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_0_0_win)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_f(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            fc_rx, #fc
            10000, #bw
            "RX", #name
            1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)


        self.qtgui_waterfall_sink_x_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_0_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            'RX Bits', #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_f(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            fc_rx, #fc
            22000, #bw
            'RX', #name
            1
        )
        self.qtgui_freq_sink_x_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0.set_y_axis(-60, 10)
        self.qtgui_freq_sink_x_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0.enable_control_panel(False)


        self.qtgui_freq_sink_x_0_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            fc_tx, #fc
            samp_rate, #bw
            "Transmitted Uplink Spectrum", #name
            1
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.nrzs_line_coding_0 = nrzs_line_coding()
        self.limesdr_source_0 = limesdr.source('1D7514D4CD338E', 0, '')


        self.limesdr_source_0.set_sample_rate(samp_rate)


        self.limesdr_source_0.set_center_freq(fc_rx, 0)

        self.limesdr_source_0.set_bandwidth(1.5e6, 0)




        self.limesdr_source_0.set_gain(rx_gain, 0)


        self.limesdr_source_0.set_antenna(255, 0)


        self.limesdr_source_0.calibrate(2.5e6, 0)
        self.limesdr_sink_0 = limesdr.sink('1D7514D4CD338E', 0, '', '')


        self.limesdr_sink_0.set_sample_rate(samp_rate)


        self.limesdr_sink_0.set_center_freq(fc_tx, 0)

        self.limesdr_sink_0.set_bandwidth(5e6, 0)


        self.limesdr_sink_0.set_digital_filter(samp_rate, 0)


        self.limesdr_sink_0.set_gain(tx_gain_56, 0)


        self.limesdr_sink_0.set_antenna(255, 0)


        self.limesdr_sink_0.calibrate(2.5e6, 0)
        self.hdlc_framer_with_preamble_0 = hdlc_framer_with_preamble(
            num_postamble_bytes=10,
            num_preamble_bytes=20,
        )
        self._fc_tx_gui_range = Range(145.90e6, 145.92e6, 100, 145.91e6, 200)
        self._fc_tx_gui_win = RangeWidget(self._fc_tx_gui_range, self.set_fc_tx_gui, 'fc_tx_gui', "counter_slider", float)
        self.top_layout.addWidget(self._fc_tx_gui_win)
        self.digital_symbol_sync_xx_0 = digital.symbol_sync_ff(
            digital.TED_SIGNUM_TIMES_SLOPE_ML,
            sps,
            0.45,
            1.0,
            1.0,
            1.5,
            1,
            digital.constellation_bpsk().base(),
            digital.IR_MMSE_8TAP,
            32,
            rrc_taps)
        self.digital_scrambler_bb_0 = digital.scrambler_bb(0x21, 0x00, 16)
        self.digital_hdlc_deframer_bp_0 = digital.hdlc_deframer_bp(16, 250)
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(4)
        self.digital_descrambler_bb_0 = digital.descrambler_bb(0x21, 0, 16)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_socket_pdu_1 = blocks.socket_pdu('UDP_CLIENT', '127.0.0.1', '27000', 10000, False)
        self.blocks_socket_pdu_0_0 = blocks.socket_pdu('UDP_SERVER', '127.0.0.1', '27001', 1000, False)
        self.blocks_not_xx_0_0 = blocks.not_bb()
        self.blocks_message_debug_1 = blocks.message_debug()
        self.blocks_message_debug_0 = blocks.message_debug()
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)
        self.blocks_and_const_xx_0_0 = blocks.and_const_bb(1)
        self.analog_simple_squelch_cc_0 = analog.simple_squelch_cc(-50, 1)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(1)
        self.analog_agc_xx_0 = analog.agc_ff(1e-6, 1.0, 1.0)
        self.analog_agc_xx_0.set_max_gain(65536)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_socket_pdu_0_0, 'pdus'), (self.blocks_message_debug_0, 'print_pdu'))
        self.msg_connect((self.blocks_socket_pdu_0_0, 'pdus'), (self.hdlc_framer_with_preamble_0, 'in'))
        self.msg_connect((self.digital_hdlc_deframer_bp_0, 'out'), (self.blocks_message_debug_1, 'print_pdu'))
        self.msg_connect((self.digital_hdlc_deframer_bp_0, 'out'), (self.blocks_socket_pdu_1, 'pdus'))
        self.connect((self.analog_agc_xx_0, 0), (self.root_raised_cosine_filter_1, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.analog_agc_xx_0, 0))
        self.connect((self.analog_simple_squelch_cc_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.blocks_and_const_xx_0_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.blocks_and_const_xx_0_0, 0), (self.digital_hdlc_deframer_bp_0, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.blocks_not_xx_0_0, 0), (self.blocks_and_const_xx_0_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.digital_diff_decoder_bb_0, 0))
        self.connect((self.digital_descrambler_bb_0, 0), (self.blocks_not_xx_0_0, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.digital_descrambler_bb_0, 0))
        self.connect((self.digital_scrambler_bb_0, 0), (self.trxv_uplink_fsk_modulator_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.qtgui_freq_sink_x_0_0, 0))
        self.connect((self.hdlc_framer_with_preamble_0, 0), (self.nrzs_line_coding_0, 0))
        self.connect((self.limesdr_source_0, 0), (self.analog_simple_squelch_cc_0, 0))
        self.connect((self.nrzs_line_coding_0, 0), (self.digital_scrambler_bb_0, 0))
        self.connect((self.root_raised_cosine_filter_1, 0), (self.digital_symbol_sync_xx_0, 0))
        self.connect((self.trxv_uplink_fsk_modulator_0, 0), (self.limesdr_sink_0, 0))
        self.connect((self.trxv_uplink_fsk_modulator_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.trxv_uplink_fsk_modulator_0, 0), (self.qtgui_waterfall_sink_x_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "limesdr_bpsk_loopback")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_baud_rate(self):
        return self.baud_rate

    def set_baud_rate(self, baud_rate):
        self.baud_rate = baud_rate
        self.set_samp_rate(self.baud_rate*self.sps)

    def get_equ_gain(self):
        return self.equ_gain

    def set_equ_gain(self, equ_gain):
        self.equ_gain = equ_gain

    def get_excess_bw(self):
        return self.excess_bw

    def set_excess_bw(self, excess_bw):
        self.excess_bw = excess_bw
        self.set_rrc_taps(firdes.root_raised_cosine(1.0,self.samp_rate,2*self.samp_rate/self.sps,self.excess_bw,11*self.sps))

    def get_fc_rx(self):
        return self.fc_rx

    def set_fc_rx(self, fc_rx):
        self.fc_rx = fc_rx
        self.limesdr_source_0.set_center_freq(self.fc_rx, 0)
        self.qtgui_freq_sink_x_0_0.set_frequency_range(self.fc_rx, 22000)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.fc_rx, 10000)

    def get_fc_tx(self):
        return self.fc_tx

    def set_fc_tx(self, fc_tx):
        self.fc_tx = fc_tx
        self.limesdr_sink_0.set_center_freq(self.fc_tx, 0)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.fc_tx, self.samp_rate)
        self.qtgui_waterfall_sink_x_0_0.set_frequency_range(self.fc_tx, 10000)

    def get_loop_bw(self):
        return self.loop_bw

    def set_loop_bw(self, loop_bw):
        self.loop_bw = loop_bw

    def get_rx_gain_default(self):
        return self.rx_gain_default

    def set_rx_gain_default(self, rx_gain_default):
        self.rx_gain_default = rx_gain_default
        self.set_rx_gain(self.rx_gain_default)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_rrc_taps(firdes.root_raised_cosine(1.0,self.samp_rate,2*self.samp_rate/self.sps,self.excess_bw,11*self.sps))
        self.set_samp_rate(self.baud_rate*self.sps)
        self.root_raised_cosine_filter_1.set_taps(firdes.root_raised_cosine(1, self.samp_rate, 2*self.samp_rate/self.sps, 0.0035, 160))
        self.trxv_uplink_fsk_modulator_0.set_sps(self.sps)

    def get_tx_gain_56(self):
        return self.tx_gain_56

    def set_tx_gain_56(self, tx_gain_56):
        self.tx_gain_56 = tx_gain_56
        self.set_tx_gain(self.tx_gain_56)
        self.limesdr_sink_0.set_gain(self.tx_gain_56, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_rrc_taps(firdes.root_raised_cosine(1.0,self.samp_rate,2*self.samp_rate/self.sps,self.excess_bw,11*self.sps))
        self.limesdr_sink_0.set_digital_filter(self.samp_rate, 0)
        self.limesdr_sink_0.set_digital_filter(self.samp_rate, 1)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.fc_tx, self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.root_raised_cosine_filter_1.set_taps(firdes.root_raised_cosine(1, self.samp_rate, 2*self.samp_rate/self.sps, 0.0035, 160))
        self.trxv_uplink_fsk_modulator_0.set_samp_rate(self.samp_rate)

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self.limesdr_source_0.set_gain(self.rx_gain, 0)

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps

    def get_fc_tx_gui(self):
        return self.fc_tx_gui

    def set_fc_tx_gui(self, fc_tx_gui):
        self.fc_tx_gui = fc_tx_gui

    def get_bpsk_obj(self):
        return self.bpsk_obj

    def set_bpsk_obj(self, bpsk_obj):
        self.bpsk_obj = bpsk_obj




def argument_parser():
    description = 'Sends data with FSK through Ettus SDR'
    parser = ArgumentParser(description=description)
    parser.add_argument(
        "--baud-rate", dest="baud_rate", type=intx, default=1200,
        help="Set baud_rate [default=%(default)r]")
    parser.add_argument(
        "--fc-rx", dest="fc_rx", type=eng_float, default="436.83M",
        help="Set fc_rx [default=%(default)r]")
    parser.add_argument(
        "--fc-tx", dest="fc_tx", type=eng_float, default="145.91M",
        help="Set fc_tx [default=%(default)r]")
    parser.add_argument(
        "--sps", dest="sps", type=intx, default=160,
        help="Set sps [default=%(default)r]")
    parser.add_argument(
        "--tx-gain-56", dest="tx_gain_56", type=intx, default=56,
        help="Set tx_gain_56 [default=%(default)r]")
    return parser


def main(top_block_cls=limesdr_bpsk_loopback, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(baud_rate=options.baud_rate, fc_rx=options.fc_rx, fc_tx=options.fc_tx, sps=options.sps, tx_gain_56=options.tx_gain_56)

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
