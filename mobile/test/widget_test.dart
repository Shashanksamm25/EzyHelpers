
import 'package:flutter_test/flutter_test.dart';
import 'package:ezyhelpers_app/main.dart';

void main() {
  testWidgets('EzyHelpers login screen loads', (WidgetTester tester) async {
    await tester.pumpWidget(const EzyHelpersApp());

    expect(find.text('EzyHelpers'), findsOneWidget);
    expect(find.text('Sign In'), findsOneWidget);
  });
}
