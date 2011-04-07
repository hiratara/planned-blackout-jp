use inc::Module::Install;

version_from 'lib/PlannedBlackoutJP.pm';
tests 't/*.t t/*/*.t t/*/*/*.t';
test_requires 'Test::More' => '0.96';
test_requires 'Test::WWW::Mechanize::PSGI';
test_requires 'Plack';
requires 'Text::MicroTemplate'; # to create Changes html
requires 'LWP'; # to download ken_all.lzh
requires 'Archive::Tar'; # to use helper/update.cgi on perl-5.8.x

auto_install;

WriteAll;
