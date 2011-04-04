use inc::Module::Install;

version_from 'lib/PlannedBlackoutJP.pm';
tests 't/*.t t/*/*.t t/*/*/*.t';
test_requires 'Test::More' => '0.96';
test_requires 'Test::WWW::Mechanize::PSGI';
test_requires 'Plack';
requires 'Text::MicroTemplate';

auto_install;

WriteAll;
