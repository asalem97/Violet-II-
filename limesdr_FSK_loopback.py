#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: limesdr FSK loopback
# Author: Abdulaziz Salem
# Copyright: 2024
# Description: Sends data with FSK through lime SDR mini
# GNU Radio version: 3.8.5.0

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from gnuradio import analog
import math
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from hdlc_framer_with_preamble import hdlc_framer_with_preamble  # grc-generated hier_block
from nrzs_line_coding import nrzs_line_coding  # grc-generated hier_block
from trxv_uplink_fsk_modulator import trxv_uplink_fsk_modulator  # grc-generated hier_block
import limesdr


class limesdr_FSK_loopback(gr.top_block):

    def __init__(self, baud_rate=1200, equ_gain=0.01, excess_bw=0.35, fc_rx=436.83e6, fc_tx=145.91e6, loop_bw=0.0628, rx_gain_default=56, sps=160, tx_gain_56=56):
        gr.top_block.__init__(self, "limesdr FSK loopback")

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
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(1.0,samp_rate,2*samp_rate/sps,excess_bw,11*sps)

        ##################################################
        # Blocks
        ##################################################
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
        self.nrzs_line_coding_0 = nrzs_line_coding()
        self.limesdr_source_0 = limesdr.source('1D7514D4CD338E', 0, '')


        self.limesdr_source_0.set_sample_rate(samp_rate)


        self.limesdr_source_0.set_center_freq(fc_rx, 0)

        self.limesdr_source_0.set_bandwidth(1.5e6, 0)




        self.limesdr_source_0.set_gain(56, 0)


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
        self.digital_symbol_sync_xx_0 = digital.symbol_sync_ff(
            digital.TED_SIGNUM_TIMES_SLOPE_ML,
            sps,
            0.450,
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
        self.blocks_message_debug_0_0 = blocks.message_debug()
        self.blocks_message_debug_0 = blocks.message_debug()
        self.blocks_and_const_xx_0_0 = blocks.and_const_bb(1)
        self.analog_simple_squelch_cc_0 = analog.simple_squelch_cc(-50, 1)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(1)
        self.analog_agc_xx_0 = analog.agc_ff(1e-6, 1.0, 1.0)
        self.analog_agc_xx_0.set_max_gain(65536)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_socket_pdu_0_0, 'pdus'), (self.blocks_message_debug_0_0, 'print_pdu'))
        self.msg_connect((self.blocks_socket_pdu_0_0, 'pdus'), (self.hdlc_framer_with_preamble_0, 'in'))
        self.msg_connect((self.digital_hdlc_deframer_bp_0, 'out'), (self.blocks_message_debug_0, 'print_pdu'))
        self.msg_connect((self.digital_hdlc_deframer_bp_0, 'out'), (self.blocks_socket_pdu_1, 'pdus'))
        self.connect((self.analog_agc_xx_0, 0), (self.root_raised_cosine_filter_1, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.analog_agc_xx_0, 0))
        self.connect((self.analog_simple_squelch_cc_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.blocks_and_const_xx_0_0, 0), (self.digital_hdlc_deframer_bp_0, 0))
        self.connect((self.blocks_not_xx_0_0, 0), (self.blocks_and_const_xx_0_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.digital_diff_decoder_bb_0, 0))
        self.connect((self.digital_descrambler_bb_0, 0), (self.blocks_not_xx_0_0, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.digital_descrambler_bb_0, 0))
        self.connect((self.digital_scrambler_bb_0, 0), (self.trxv_uplink_fsk_modulator_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.hdlc_framer_with_preamble_0, 0), (self.nrzs_line_coding_0, 0))
        self.connect((self.limesdr_source_0, 0), (self.analog_simple_squelch_cc_0, 0))
        self.connect((self.nrzs_line_coding_0, 0), (self.digital_scrambler_bb_0, 0))
        self.connect((self.root_raised_cosine_filter_1, 0), (self.digital_symbol_sync_xx_0, 0))
        self.connect((self.trxv_uplink_fsk_modulator_0, 0), (self.limesdr_sink_0, 0))


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

    def get_fc_tx(self):
        return self.fc_tx

    def set_fc_tx(self, fc_tx):
        self.fc_tx = fc_tx
        self.limesdr_sink_0.set_center_freq(self.fc_tx, 0)

    def get_loop_bw(self):
        return self.loop_bw

    def set_loop_bw(self, loop_bw):
        self.loop_bw = loop_bw

    def get_rx_gain_default(self):
        return self.rx_gain_default

    def set_rx_gain_default(self, rx_gain_default):
        self.rx_gain_default = rx_gain_default

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
        self.limesdr_sink_0.set_gain(self.tx_gain_56, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_rrc_taps(firdes.root_raised_cosine(1.0,self.samp_rate,2*self.samp_rate/self.sps,self.excess_bw,11*self.sps))
        self.limesdr_sink_0.set_digital_filter(self.samp_rate, 0)
        self.limesdr_sink_0.set_digital_filter(self.samp_rate, 1)
        self.root_raised_cosine_filter_1.set_taps(firdes.root_raised_cosine(1, self.samp_rate, 2*self.samp_rate/self.sps, 0.0035, 160))
        self.trxv_uplink_fsk_modulator_0.set_samp_rate(self.samp_rate)

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps




def argument_parser():
    description = 'Sends data with FSK through lime SDR mini'
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


def main(top_block_cls=limesdr_FSK_loopback, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(baud_rate=options.baud_rate, fc_rx=options.fc_rx, fc_tx=options.fc_tx, sps=options.sps, tx_gain_56=options.tx_gain_56)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
