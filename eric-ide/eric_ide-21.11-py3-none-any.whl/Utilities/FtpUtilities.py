# -*- coding: utf-8 -*-

# Copyright (c) 2012 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing some FTP related utilities.
"""

import os

from PyQt5.QtCore import QObject, QDate, QDateTime, QTime

from E5Network.E5UrlInfo import E5UrlInfo, E5UrlPermission


class FtpDirLineParserError(Exception):
    """
    Exception class raised, if a parser issue was detected.
    """
    pass


class FtpDirLineParser(QObject):
    """
    Class to parse lines returned by a FTP LIST command.
    """
    MonthnamesNumbers = {
        "jan": 1,
        "feb": 2,
        "mar": 3,
        "apr": 4,
        "may": 5,
        "jun": 6,
        "jul": 7,
        "aug": 8,
        "sep": 9,
        "oct": 10,
        "nov": 11,
        "dec": 12,
    }
    
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent object (QObject)
        """
        super().__init__(parent)
        
        self.__parseLine = self.__parseUnixLine
        self.__modeSwitchAllowed = True
    
    def __ignoreLine(self, line):
        """
        Private method to check, if the line should be ignored.
        
        @param line to check (string)
        @return flag indicating to ignore the line (boolean)
        """
        return (
            line.strip() == "" or
            line.strip().lower().startswith("total ")
        )
    
    def __parseUnixMode(self, modeString, urlInfo):
        """
        Private method to parse a Unix mode string modifying the
        given URL info object.
        
        @param modeString mode string to be parsed (string)
        @param urlInfo reference to the URL info object (E5UrlInfo)
        @exception FtpDirLineParserError Raised if the mode cannot be parsed.
        """
        if len(modeString) != 10:
            raise FtpDirLineParserError(
                "invalid mode string '{0}'".format(modeString))
        
        modeString = modeString.lower()
        
        permission = 0
        if modeString[1] != '-':
            permission |= E5UrlPermission.READ_OWNER
        if modeString[2] != '-':
            permission |= E5UrlPermission.WRITE_OWNER
        if modeString[3] != '-':
            permission |= E5UrlPermission.EXE_OWNER
        if modeString[4] != '-':
            permission |= E5UrlPermission.READ_GROUP
        if modeString[5] != '-':
            permission |= E5UrlPermission.WRITE_GROUP
        if modeString[6] != '-':
            permission |= E5UrlPermission.EXE_GROUP
        if modeString[7] != '-':
            permission |= E5UrlPermission.READ_OTHER
        if modeString[8] != '-':
            permission |= E5UrlPermission.WRITE_OTHER
        if modeString[9] != '-':
            permission |= E5UrlPermission.EXE_OTHER
        urlInfo.setPermissions(permission)
        
        if modeString[0] == "d":
            urlInfo.setDir(True)
            urlInfo.setFile(False)
            urlInfo.setSymLink(False)
        elif modeString[0] == "l":
            urlInfo.setDir(True)
            urlInfo.setFile(False)
            urlInfo.setSymLink(True)
        elif modeString[0] == "-":
            urlInfo.setDir(False)
            urlInfo.setFile(True)
            urlInfo.setSymLink(False)
    
    def __parseUnixTime(self, monthAbbreviation, day, yearOrTime, urlInfo):
        """
        Private method to parse a Unix date and time indication modifying
        the given URL info object.
        

        Date time strings in Unix-style directory listings typically
        have one of these formats:
        <ul>
          <li>"Nov 23 02:33" (month name, day of month, time)</li>
          <li>"May 26  2005" (month name, day of month, year)</li>
        </ul>
        
        @param monthAbbreviation abbreviation of the month name (string)
        @param day day of the month (string)
        @param yearOrTime string giving the year or a time (string)
        @param urlInfo reference to the URL info object (E5UrlInfo)
        @exception FtpDirLineParserError Raised if the month abbreviation is
            not recognized.
        """
        try:
            month = FtpDirLineParser.MonthnamesNumbers[
                monthAbbreviation.lower()]
        except KeyError:
            raise FtpDirLineParserError(
                "illegal month abbreviation '{0}'".format(
                    monthAbbreviation))
        day = int(day)
        if ':' in yearOrTime:
            year = QDate.currentDate().year()
            hour, minute = yearOrTime.split(':')
            hour = int(hour)
            minute = int(minute)
        else:
            year = int(yearOrTime)
            hour = 0
            minute = 0
        
        lastModified = QDateTime(QDate(year, month, day), QTime(hour, minute))
        urlInfo.setLastModified(lastModified)
    
    def __splitUnixLine(self, line):
        """
        Private method to split a line of a Unix like directory listing.
       
        It splits the line into meta data, number of links, user, group, size,
        month, day, year or time and name.
        
        @param line directory line to split (string)
        @return tuple of nine strings giving the meta data,
            number of links, user, group, size, month, day, year or time
            and name
        @exception FtpDirLineParserError Raised if the line is not of a
            recognized Unix format.
        """
        # This method encapsulates the recognition of an unusual
        # Unix format variant.
        lineParts = line.split()
        fieldCountWithoutUserID = 8
        fieldCountWithUserID = fieldCountWithoutUserID + 1
        if len(lineParts) < fieldCountWithoutUserID:
            raise FtpDirLineParserError(
                "line '{0}' cannot be parsed".format(line))
        
        # If we have a valid format (either with or without user id field),
        # the field with index 5 is either the month abbreviation or a day.
        try:
            int(lineParts[5])
        except ValueError:
            # Month abbreviation, "invalid literal for int"
            lineParts = line.split(None, fieldCountWithUserID - 1)
        else:
            # Day
            lineParts = line.split(None, fieldCountWithoutUserID - 1)
            userFieldIndex = 2
            lineParts.insert(userFieldIndex, "")
        
        return lineParts
    
    def __parseUnixLine(self, line):
        """
        Private method to parse a Unix style directory listing line.
        
        @param line directory line to be parsed (string)
        @return URL info object containing the valid data (E5UrlInfo)
        """
        modeString, nlink, user, group, size, month, day, yearOrTime, name = (
            self.__splitUnixLine(line)
        )
        
        if name in [".", ".."]:
            return None
        
        urlInfo = E5UrlInfo()
        self.__parseUnixMode(modeString, urlInfo)
        self.__parseUnixTime(month, day, yearOrTime, urlInfo)
        urlInfo.setOwner(user)
        urlInfo.setGroup(group)
        urlInfo.setSize(int(size))
        name = name.strip()
        i = name.find(" -> ")
        if i >= 0:
            name = name[:i]
        urlInfo.setName(name)
        
        return urlInfo
    
    def __parseWindowsTime(self, date, time, urlInfo):
        """
        Private method to parse a Windows date and time indication modifying
        the given URL info object.

        Date time strings in Windows-style directory listings typically
        have the format "10-23-12 03:25PM" (month-day_of_month-two_digit_year,
        hour:minute, am/pm).
        
        @param date date string (string)
        @param time time string (string)
        @param urlInfo reference to the URL info object (E5UrlInfo)
        @exception FtpDirLineParserError Raised if either of the strings is not
            recognized.
        """
        try:
            month, day, year = [int(part) for part in date.split('-')]
            year = 1900 + year if year >= 70 else 2000 + year
        except (ValueError, IndexError):
            raise FtpDirLineParserError(
                "illegal date string '{0}'".format(month))
        try:
            hour, minute, am_pm = time[0:2], time[3:5], time[5]
            hour = int(hour)
            minute = int(minute)
        except (ValueError, IndexError):
            raise FtpDirLineParserError(
                "illegal time string '{0}'".format(month))
        if hour == 12 and am_pm == 'A':
            hour = 0
        if hour != 12 and am_pm == 'P':
            hour += 12
        
        lastModified = QDateTime(QDate(year, month, day), QTime(hour, minute))
        urlInfo.setLastModified(lastModified)
    
    def __parseWindowsLine(self, line):
        """
        Private method to parse a Windows style directory listing line.
        
        @param line directory line to be parsed (string)
        @return URL info object containing the valid data (E5UrlInfo)
        @exception FtpDirLineParserError Raised if the line is not of a
            recognized Windows format.
        """
        try:
            date, time, dirOrSize, name = line.split(None, 3)
        except ValueError:
            # "unpack list of wrong size"
            raise FtpDirLineParserError(
                "line '{0}' cannot be parsed".format(line))
        
        if name in [".", ".."]:
            return None
        
        urlInfo = E5UrlInfo()
        self.__parseWindowsTime(date, time, urlInfo)
        if dirOrSize.lower() == "<dir>":
            urlInfo.setDir(True)
            urlInfo.setFile(False)
        else:
            urlInfo.setDir(False)
            urlInfo.setFile(True)
            try:
                urlInfo.setSize(int(dirOrSize))
            except ValueError:
                raise FtpDirLineParserError(
                    "illegal size '{0}'".format(dirOrSize))
        urlInfo.setName(name)
        
        ext = os.path.splitext(name.lower())[1]
        urlInfo.setSymLink(ext == ".lnk")
        
        permissions = (
            E5UrlPermission.READ_OWNER | E5UrlPermission.WRITE_OWNER |
            E5UrlPermission.READ_GROUP | E5UrlPermission.WRITE_GROUP |
            E5UrlPermission.READ_OTHER | E5UrlPermission.WRITE_OTHER
        )
        if ext in [".exe", ".com", ".bat", ".cmd"]:
            permissions |= (
                E5UrlPermission.EXE_OWNER |
                E5UrlPermission.EXE_GROUP |
                E5UrlPermission.EXE_OTHER
            )
        urlInfo.setPermissions(permissions)
        
        return urlInfo
    
    def parseLine(self, line):
        """
        Public method to parse a directory listing line.
        
        This implementation support Unix and Windows style directory
        listings. It tries Unix style first and if that fails switches
        to Windows style. If that fails as well, an exception is raised.
        
        @param line directory line to be parsed (string)
        @return URL info object containing the valid data (E5UrlInfo)
        """
        if self.__ignoreLine(line):
            return None
        
        try:
            return self.__parseLine(line)
        except FtpDirLineParserError:
            if not self.__modeSwitchAllowed:
                raise
            
            self.__parseLine = self.__parseWindowsLine
            self.__modeSwitchAllowed = False
            return self.__parseLine(line)
