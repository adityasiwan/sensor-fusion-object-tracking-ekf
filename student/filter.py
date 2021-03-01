# ---------------------------------------------------------------------
# Project "Track 3D-Objects Over Time"
# Copyright (C) 2020, Dr. Antje Muntzinger / Dr. Andreas Haja.
#
# Purpose of this file : Kalman filter class
#
# You should have received a copy of the Udacity license together with this program.
#
# https://www.udacity.com/course/self-driving-car-engineer-nanodegree--nd013
# ----------------------------------------------------------------------
#

# imports
import numpy as np

# add project directory to python path to enable relative imports
import os
import sys
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
import misc.params as params

class Filter:
    '''Kalman filter class'''
    def __init__(self):
        pass

    def F(self):
        ############
        # TODO Step 1: implement and return system matrix F
        ############

        mat = np.identity(params.dim_state)
        mat[np.eye(len(mat), k=3, dtype='bool')] = params.dt

        return mat
        ############
        # END student code
        ############

    def Q(self):
        ############
        # TODO Step 1: implement and return process noise covariance Q
        ############
        mat = np.zeros((params.dim_state, params.dim_state))
        np.fill_diagonal(mat, params.dt * params.q)
        return mat

        ############
        # END student code
        ############

    def predict(self, track):
        ############
        # TODO Step 1: predict state x and estimation error covariance P to next timestep, save x and P in track
        ############

        F = self.F()
        X = F * track.x
        Q = self.Q()
        P = F * track.P * F.transpose() + Q

        track.set_x(X)
        track.set_P(P)

        ############
        # END student code
        ############

    def update(self, track, meas):
        ############
        # TODO Step 1: update state x and covariance P with associated measurement, save x and P in track
        ############
        x = track.x
        P = track.P
        H = meas.sensor.get_H(x)
        gamma = self.gamma(track, meas)
        S = self.S(track, meas, H)
        K = P * H.transpose() * np.linalg.inv(S)
        I = np.identity(params.dim_state)
        x = x + K * gamma
        P = (I - K * H) * P

        track.set_x(x)
        track.set_P(P)
        ############
        # END student code
        ############
        track.update_attributes(meas)

    def gamma(self, track, meas):
        ############
        # TODO Step 1: calculate and return residual gamma
        ############

        return meas.z - meas.sensor.get_hx(track.x)

        ############
        # END student code
        ############

    def S(self, track, meas, H):
        ############
        # TODO Step 1: calculate and return covariance of residual S
        ############

        return (H * track.P * H.transpose()) + meas.R

        ############
        # END student code
        ############ 